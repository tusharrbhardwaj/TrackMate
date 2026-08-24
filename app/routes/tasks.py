from flask import Blueprint, render_template, redirect, url_for, flash;
from flask_login import login_required, current_user;
from app import db;
from app.forms.task import TaskForm;
from app.models.goal import Goal;
from app.models.task import Task;


tasks_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)

@tasks_bp.route("/create/<int:goal_id>", methods=["GET", "POST"])
@tasks_bp.route("/create-goal/<int:goal_id>", methods=["GET", "POST"])
@login_required
def create_task(goal_id):
    goal = db.session.get(Goal, goal_id)
    if goal is None:
        return "Goal not found", 404
    if goal.owner_id != current_user.id:
        return "Access denied", 403
    
    form = TaskForm()

    if form.validate_on_submit():
        current_weight = sum(
            task.weight for task in goal.tasks
        )
        new_weight = current_weight + form.weight.data

        if new_weight > 100:
            flash(
                f"Task weights cannot be more than 100%. "
                f"Currently used: {current_weight}%.",
                "error"
            )
            return render_template(
                "create_task.html",
                form=form,
                goal=goal
            )
        task = Task(
            goal_id=goal.id,
            title=form.title.data,
            description=form.description.data,
            deadline=form.deadline.data,
            weight=form.weight.data
        )

        db.session.add(task)
        db.session.commit()

        flash("Task created successfully.", "success")
        return redirect(
            url_for("goals.view_goal", goal_id=goal.id)
        )
    return render_template(
        "create_task.html",
        form=form,
        goal=goal
    )