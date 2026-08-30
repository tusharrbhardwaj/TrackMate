from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.forms.goal import GoalForm
from app.models.goal import Goal
from app.models.user import User
from app.models.friendship import Friendship
from app.models.task import Task
from app.models.proof import Proof


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

        goal = Goal(
            owner_id=current_user.id,
            title=form.title.data,
            description=form.description.data
        )

        db.session.add(goal)
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

    # This logic is used set a friend supervisor from alrady made friends on the application
    if goal is None:
        return "Goal not found", 404

    if (
    goal.owner_id != current_user.id
    and goal.supervisor_id != current_user.id
    ):
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


    # Delete proofs first, then tasks
    for task in list(goal.tasks):

        for proof in list(task.proofs):
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