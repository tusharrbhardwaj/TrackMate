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