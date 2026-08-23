# Goal realted tests
from app import db
from app.models.goal import Goal


def create_user_and_login(client):
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

def test_create_goal(client, app):
    create_user_and_login(client)
    response = client.post(
        "/goals/create",
        data={
            "title": "Become US President",
            "description": "Get USA citizenship, marry Trumps daughter, ask him to invest in you."
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Goal created successfully." in response.data
    assert b"Become US President" in response.data


def test_goal_belongs_to_user(client, app):
    create_user_and_login(client)
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
        assert goal.owner.username == "misha"

def test_wrong_goal(client, app):
    create_user_and_login(client)
    response = client.post(
        "/goals/create",
        data={
            "title": "",
            "description": "Mi mi ma mo mu."
        }
    )
    assert response.status_code == 200
    assert b"This field is required." in response.data
