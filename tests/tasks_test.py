from app import db
from app.models.goal import Goal
from app.models.task import Task


def create_user_and_goal(client, app):
    client.post(
        "/register",
        data={
            "username": "misha",
            "email": "misha@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
    )
    client.post(
        "/login",
        data={
            "email": "misha@example.com",
            "password": "password123",
        }
    )
    client.post(
        "/goals/create",
        data={
            "title": "Become US President",
            "description": "Get USA citizenship, marry Trumps daughter, ask him to invest in you."
        }
    )
    with app.app_context():
        goal = db.session.execute(
            db.select(Goal).where(
                Goal.title == "Become US President"
            )
        ).scalar_one()
        return goal.id


# Task creation test
def test_create_task(client, app):
    goal_id = create_user_and_goal(client, app)
    response = client.post(
        f"/tasks/create/{goal_id}",
        data={
            "title": "Fly to USA",
            "description": "Go get a ticket.",
            "deadline": "2026-08-25T18:00"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Task created successfully." in response.data
    assert b"Fly to USA" in response.data


# Task should belong to a specific goal
def test_task_belongs_to_goal(client, app):
    goal_id = create_user_and_goal(client, app)
    client.post(
        f"/tasks/create/{goal_id}",
        data={
            "title": "Fly to USA",
            "description": "Go get a ticket.",
            "deadline": "2026-08-25T18:00"
        }
    )
    with app.app_context():
        task = db.session.execute(
            db.select(Task).where(
                Task.title == "Fly to USA"
            )
        ).scalar_one()
        assert task.goal_id == goal_id


# Task should have a title
def test_task_requires_title(client, app):
    goal_id = create_user_and_goal(client, app)
    response = client.post(
        f"/tasks/create/{goal_id}",
        data={
            "title": "",
            "description": "Go get a ticket.",
            "deadline": "2026-08-25T18:00"
        }
    )
    assert response.status_code == 200
    assert b"This field is required." in response.data


def test_create_task_requires_login(client, app):
    with app.app_context():
        goal = Goal(
            owner_id=1,
            title="Test Goal",
            description="Test"
        )
        db.session.add(goal)
        db.session.commit()
        goal_id = goal.id
    response = client.get(
        f"/tasks/create/{goal_id}",
        follow_redirects=True
    )
    assert b"Log In" in response.data