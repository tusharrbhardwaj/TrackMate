import os

from flask import Blueprint, current_app, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.forms.goal import GoalForm
from app.models.goal import Goal
from app.models.user import User
from app.models.friendship import Friendship
from app.models.task import Task
from app.models.proof import Proof
from app.core_adapter import as_core_goal, as_goal_model
from trackmate_lib import CreateGoal, ForbiddenError, GoalService, NotFoundError


goals_bp = Blueprint(
    "goals",
    __name__,
    url_prefix="/goals"
)


@goals_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@goals_bp.route(
    "/create-goal",
    methods=["GET", "POST"]
)
@login_required
def create_goal():

    form = GoalForm()

    if form.validate_on_submit():
        core_goal = GoalService.create(
            current_user.id,
            CreateGoal(form.title.data, form.description.data),
        )
        db.session.add(as_goal_model(core_goal))
        db.session.commit()

        flash(
            "Goal created successfully.",
            "success"
        )

        return redirect(
            url_for("auth.home")
        )

    return render_template(
        "create_goal.html",
        form=form
    )


# Reviwing goal

@goals_bp.route("/<int:goal_id>")
@login_required
def view_goal(goal_id):
    goal = db.session.get(
        Goal,
        goal_id
    )

    try:
        GoalService.require_visible(as_core_goal(goal), current_user.id)
    except NotFoundError:
        return "Goal not found", 404
    except ForbiddenError:
        return "Access denied", 403


    # Find all accepted friendships
    friendships = db.session.execute(

        db.select(Friendship).where(

            (
                (Friendship.sender_id == current_user.id)
                |
                (Friendship.receiver_id == current_user.id)
            ),

            Friendship.status == "ACCEPTED"

        )

    ).scalars().all()


    # Convert friendship objects into actual User objects
    friends = []

    for friendship in friendships:

        if friendship.sender_id == current_user.id:

            friends.append(
                friendship.receiver
            )

        else:

            friends.append(
                friendship.sender
            )


    return render_template(
        "goal.html",
        goal=goal,
        friends=friends
    )


#Assigning firend supervisor

@goals_bp.route(
    "/<int:goal_id>/supervisor/<int:user_id>",
    methods=["POST"]
)
@login_required
def assign_supervisor(goal_id, user_id):

    goal = db.session.get(
        Goal,
        goal_id
    )

    if goal is None:
        return "Goal not found", 404


    # Only goal owner can assign supervisor
    if goal.owner_id != current_user.id:
        return "Access denied", 403


    target_user = db.session.get(
        User,
        user_id
    )

    if target_user is None:
        return "User not found", 404


    # Make sure they are actually friends
    friendship = db.session.execute(

        db.select(Friendship).where(

            Friendship.status == "ACCEPTED",

            (
                (
                    (Friendship.sender_id == current_user.id)
                    &
                    (Friendship.receiver_id == target_user.id)
                )

                |

                (
                    (Friendship.sender_id == target_user.id)
                    &
                    (Friendship.receiver_id == current_user.id)
                )
            )

        )

    ).scalar_one_or_none()


    if friendship is None:

        flash(
            "You can only choose one of your friends as supervisor.",
            "error"
        )

        return redirect(
            url_for(
                "goals.view_goal",
                goal_id=goal.id
            )
        )


    goal.supervisor_id = target_user.id

    db.session.commit()


    flash(
        f"{target_user.username} is now supervising this goal.",
        "success"
    )


    return redirect(
        url_for(
            "goals.view_goal",
            goal_id=goal.id
        )
    )
    
# DELETE GOAL

@goals_bp.route(
    "/<int:goal_id>/delete",
    methods=["POST"]
)
@login_required
def delete_goal(goal_id):

    goal = db.session.get(
        Goal,
        goal_id
    )

    if goal is None:
        return "Goal not found", 404


    # Only the owner can delete the goal
    if goal.owner_id != current_user.id:
        return "Access denied", 403


    # Delete proofs first, then tasks.
    tasks = db.session.execute(
        db.select(Task).where(Task.goal_id == goal.id)
    ).scalars().all()

    for task in tasks:

        proofs = db.session.execute(
            db.select(Proof).where(Proof.task_id == task.id)
        ).scalars().all()

        for proof in proofs:
            photo_file = os.path.join(
                current_app.config["PROOF_UPLOAD_FOLDER"],
                os.path.basename(proof.photo_path)
            )
            if os.path.exists(photo_file):
                os.remove(photo_file)
            db.session.delete(proof)

        db.session.delete(task)


    # Finally delete the goal
    db.session.delete(goal)

    db.session.commit()


    flash(
        f'Goal "{goal.title}" deleted successfully.',
        "success"
    )


    return redirect(
        url_for("auth.home")
    )
