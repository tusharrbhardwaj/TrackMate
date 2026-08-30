import uuid
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import login_required, current_user
from app import db
from datetime import datetime, timezone
from app.models.task import Task
from app.models.proof import Proof
from app.forms.proof import ProofForm
from app.models.goal import Goal
from app.supabase import supabase


proof_bp = Blueprint(
    "proof",
    __name__,
    url_prefix="/proof"
)


@proof_bp.route(
    "/submit/<int:task_id>",
    methods=["GET", "POST"]
)
@login_required
def submit_proof(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return "Task not found", 404
    if task.goal.owner_id != current_user.id:
        return "Access denied", 403

    # Making sure that user didnt upload a proof before
    existing_proof = db.session.execute(
    db.select(Proof).where(
        Proof.task_id == task.id,
        Proof.user_id == current_user.id,
        Proof.status == "PENDING"
        )
    ).scalar_one_or_none()

    if existing_proof:
        flash(
            "You already have a proof waiting for review.",
            "error"
        )
        return redirect(
            url_for(
                "goals.view_goal",
                goal_id=task.goal_id
            )
        )
    
    form = ProofForm()

    if form.validate_on_submit():
        # Check description length 100 words max
        word_count = len(
            form.description.data.split()
        )
        if word_count < 100:
            flash(
                "Explanation must contain at least 100 words.",
                "error"
            )
            return render_template(
                "proof.html",
                form=form,
                task=task
            )
        # Create a unique filename
        file = form.photo.data
        filename = (
            str(uuid.uuid4())
            + "_"
            + file.filename
        )
        # Upload image to Supabase 
        supabase.storage.from_("proofs").upload(
            filename,
            file.read(),
            {
                "content-type": file.content_type
            }
        )
        # Create Proof record
        proof = Proof(
            task_id=task.id,
            user_id=current_user.id,
            description=form.description.data,
            photo_path=filename,
            status="PENDING"
        )

        db.session.add(proof)
        task.status = "PENDING_REVIEW"
        db.session.commit()
        flash(
            "Proof submitted successfully.",
            "success"
        )
        return redirect(
            url_for(
                "goals.view_goal",
                goal_id=task.goal_id
            )
        )
    return render_template(
        "proof.html",
        form=form,
        task=task
    )
    
#supervisor review page

@proof_bp.route("/reviews")
@login_required
def reviews():

    pending_proofs = db.session.execute(

        db.select(Proof)
        .join(Task, Proof.task_id == Task.id)
        .join(Goal, Task.goal_id == Goal.id)
        .where(
            Goal.supervisor_id == current_user.id,
            Proof.status == "PENDING"
        )

    ).scalars().all()


    review_items = []

    for proof in pending_proofs:

        photo_url = None

        try:

            signed = (
                supabase.storage
                .from_("proofs")
                .create_signed_url(
                    proof.photo_path,
                    3600
                )
            )

            photo_url = (
                signed.get("signedURL")
                or signed.get("signed_url")
                or signed.get("url")
            )

        except Exception as error:

            print(
                "Could not create proof image URL:",
                error
            )


        review_items.append(
            {
                "proof": proof,
                "photo_url": photo_url
            }
        )


    return render_template(
        "reviews.html",
        review_items=review_items
    )


#aproove proof system

@proof_bp.route(
    "/approve/<int:proof_id>",
    methods=["POST"]
)
@login_required
def approve_proof(proof_id):

    proof = db.session.get(
        Proof,
        proof_id
    )


    if proof is None:

        return "Proof not found", 404


    # ONLY assigned supervisor can review it
    if proof.task.goal.supervisor_id != current_user.id:

        return "Access denied", 403


    if proof.status != "PENDING":

        flash(
            "This proof has already been reviewed.",
            "error"
        )

        return redirect(
            url_for("proof.reviews")
        )


    proof.status = "APPROVED"

    proof.task.status = "COMPLETED"

    proof.task.completed_at = datetime.now(
        timezone.utc
    )

    # Owner receives +1 rating
    proof.user.rating += 1


    db.session.commit()


    flash(
        f"Proof approved. {proof.user.username} received +1 rating.",
        "success"
    )


    return redirect(
        url_for("proof.reviews")
    )


#decline proof

@proof_bp.route(
    "/reject/<int:proof_id>",
    methods=["POST"]
)
@login_required
def reject_proof(proof_id):

    proof = db.session.get(
        Proof,
        proof_id
    )


    if proof is None:

        return "Proof not found", 404


    # ONLY assigned supervisor can review it
    if proof.task.goal.supervisor_id != current_user.id:

        return "Access denied", 403


    if proof.status != "PENDING":

        flash(
            "This proof has already been reviewed.",
            "error"
        )

        return redirect(
            url_for("proof.reviews")
        )


    proof.status = "REJECTED"

    proof.task.status = "ACTIVE"

    proof.task.completed_at = None

    # Owner loses 1 rating
    proof.user.rating -= 1


    db.session.commit()


    flash(
        f"Proof rejected. {proof.user.username} received -1 rating.",
        "success"
    )


    return redirect(
        url_for("proof.reviews")
    )