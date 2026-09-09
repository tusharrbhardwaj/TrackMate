from datetime import datetime

import pytest

from trackmate_lib import (
    AllocationExceededError,
    CreateTask,
    ForbiddenError,
    Goal,
    GoalService,
    Task,
    TaskService,
)


def test_supervisor_can_view_goal():
    goal = Goal(1, owner_id=10, title="Read", description=None, supervisor_id=20)

    assert GoalService.require_visible(goal, actor_id=20) == goal


def test_other_user_cannot_view_goal():
    goal = Goal(1, owner_id=10, title="Read", description=None)

    with pytest.raises(ForbiddenError):
        GoalService.require_visible(goal, actor_id=30)


def test_task_allocation_cannot_exceed_one_hundred_percent():
    goal = Goal(1, owner_id=10, title="Read", description=None)
    existing_task = Task(1, 1, "First", None, datetime.now(), 100)

    with pytest.raises(AllocationExceededError):
        TaskService.create(
            goal,
            [existing_task],
            actor_id=10,
            command=CreateTask("Second", None, datetime.now(), 1),
        )
