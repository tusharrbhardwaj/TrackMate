from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.core_adapter import as_core_goal, as_core_task, as_task_model
from app.forms.task import TaskForm
from app.models.goal import Goal
from trackmate_lib import (
    AllocationExceededError,
    CreateTask,
    ForbiddenError,
    NotFoundError,
    TaskService,
)


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
    core_goal = as_core_goal(goal)
    try:
        TaskService.require_owner(core_goal, current_user.id)
    except NotFoundError:
        return "Goal not found", 404
    except ForbiddenError:
        return "Access denied", 403
    
    form = TaskForm()

    if form.validate_on_submit():
        try:
            core_task = TaskService.create(
                core_goal,
                [as_core_task(task) for task in goal.tasks],
                current_user.id,
                CreateTask(
                    form.title.data,
                    form.description.data,
                    form.deadline.data,
                    form.weight.data,
                ),
            )
        except AllocationExceededError as error:
            flash(
                f"Task weights cannot be more than 100%. "
                f"Currently used: {error.current_weight}%.",
                "error"
            )
            return render_template(
                "create_task.html",
                form=form,
                goal=goal
            )
        db.session.add(as_task_model(core_task))
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
