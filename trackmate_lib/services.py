"""Small, reusable goal and task rules."""

from .entities import CreateGoal, CreateTask, Goal, Task
from .errors import AllocationExceededError, ForbiddenError, NotFoundError


class GoalService:
    @staticmethod
    def create(owner_id: int, command: CreateGoal) -> Goal:
        return Goal(None, owner_id, command.title, command.description)

    @staticmethod
    def require_visible(goal: Goal | None, actor_id: int) -> Goal:
        if goal is None:
            raise NotFoundError("Goal not found")
        if actor_id not in (goal.owner_id, goal.supervisor_id):
            raise ForbiddenError("Access denied")
        return goal


class TaskService:
    @staticmethod
    def require_owner(goal: Goal | None, actor_id: int) -> Goal:
        if goal is None:
            raise NotFoundError("Goal not found")
        if goal.owner_id != actor_id:
            raise ForbiddenError("Access denied")
        return goal

    @staticmethod
    def create(
        goal: Goal | None,
        existing_tasks: list[Task],
        actor_id: int,
        command: CreateTask,
    ) -> Task:
        goal = TaskService.require_owner(goal, actor_id)

        current_weight = sum(task.weight for task in existing_tasks)
        if current_weight + command.weight > 100:
            raise AllocationExceededError(current_weight)

        return Task(
            None,
            goal.id,
            command.title,
            command.description,
            command.deadline,
            command.weight,
        )
