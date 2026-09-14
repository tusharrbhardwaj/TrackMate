# Authentification realted tests

from app import db
from app.models.user import User;

# Test registration process
def test_successful_registration(client, app):
    response = client.post(
        "/register",
        data={
            "username": "sambo",
            "email": "sambo@example.com",
            "password": "thesambo123",
            "confirm_password": "thesambo123",
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Registration Successful" in response.data

    with app.app_context():
        user = db.session.execute(
            db.select(User).where(User.username == "sambo")
        ).scalar_one_or_none()

        assert user is not None
        assert user.email == "sambo@example.com"
        assert user.password_hash != "thesambo123"

# Testing wrong email address
def test_invalid_email(client):
    response = client.post(
        "/register",
        data={
            "username": "sambo",
            "email": "aleshasha",
            "password": "password123",
            "confirm_password": "password123",
        }
    )
    assert response.status_code == 200
    assert b"Invalid email address" in response.data


# Testing successfull login with right login credentials
def test_successful_login(client, app):
    client.post(
        "/register",
        data={
            "username": "misha",
            "email": "misha@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
    )
    response = client.post(
        "/login",
        data={
            "email": "misha@example.com",
            "password": "password123",
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome to TrackMate" in response.data

    with client.session_transaction() as session:
        assert "_user_id" in session

# User should be loged in to enter home page
def test_home_requires_login(client):
    response = client.get(
        "/home",
        follow_redirects=True
    )
    assert b"Log In" in response.data
