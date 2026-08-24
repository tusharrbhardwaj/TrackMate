from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.forms.goal import GoalForm
from app.models.goal import Goal;

goals_bp = Blueprint(
    "goals",
    __name__,
    url_prefix="/goals"
)

@goals_bp.route("/create", methods=["GET", "POST"])
@goals_bp.route("/create-goal", methods=["GET", "POST"])
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
        flash("Goal created successfully.", "success")
        return redirect(url_for("auth.home"))
    return render_template(
        "create_goal.html",
        form=form
    )


@goals_bp.route("/<int:goal_id>")
@login_required
def view_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if goal is None:
        return "Goal not found", 404
    if goal.owner_id != current_user.id:
        return "Access denied", 403
    return render_template(
        "goal.html",
        goal=goal
    )