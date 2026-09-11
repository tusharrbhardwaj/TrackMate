"""The only bridge between ORM models and the reusable core data objects."""

from app.models.goal import Goal as GoalModel
from app.models.task import Task as TaskModel
from trackmate_lib import Goal, Task


def as_core_goal(goal: GoalModel | None) -> Goal | None:
    if goal is None:
        return None
    return Goal(
        goal.id,
        goal.owner_id,
        goal.title,
        goal.description,
        goal.supervisor_id,
    )


def as_core_task(task: TaskModel) -> Task:
    return Task(
        task.id,
        task.goal_id,
        task.title,
        task.description,
        task.deadline,
        task.weight,
    )


def as_goal_model(goal: Goal) -> GoalModel:
    return GoalModel(
        owner_id=goal.owner_id,
        title=goal.title,
        description=goal.description,
        supervisor_id=goal.supervisor_id,
    )


def as_task_model(task: Task) -> TaskModel:
    return TaskModel(
        goal_id=task.goal_id,
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        weight=task.weight,
    )
