# Profile realted tests

from app import db;
from app.models.user import User;

# Helper creation
def create_user(client, app):
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

# Test login required before accessing the profile page
def test_profile_requires_login(client):
    response = client.get(
        "/profile/",
        follow_redirects=True
    )
    assert b"Log In" in response.data

#User can view profile
def test_view_profile(client, app):
    create_user(client, app)
    response = client.get("/profile/")
    assert response.status_code == 200
    assert b"My Profile" in response.data
    assert b"misha" in response.data
    assert b"misha@example.com" in response.data

#Changing user credentials test
def test_update_profile(client, app):
    create_user(client, app)
    response = client.post(
        "/profile/",
        data={
            "username": "trump",
            "email": "trump@example.com",
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Profile updated successfully." in response.data
    with app.app_context():
        user = db.session.execute(
            db.select(User).where(
                User.username == "trump"
            )
        ).scalar_one_or_none()
        assert user is not None
        assert user.email == "trump@example.com"

# User name exists test
def test_duplicate_username_rejected(client, app):
    create_user(client, app)
    with app.app_context():
        second_user = User(
            username="alex",
            email="alex@example.com",
            password_hash="alex_password"
        )
        db.session.add(second_user)
        db.session.commit()

    response = client.post(
        "/profile/",
        data={
            "username": "alex",
            "email": "misha@example.com",
        },
        follow_redirects=True
    )
    assert b"Username or email already exists." in response.data

# Invalid email test
def test_invalid_email_rejected(client, app):
    create_user(client, app)
    response = client.post(
        "/profile/",
        data={
            "username": "misha",
            "email": "loollypop",
        }
    )
    assert response.status_code == 200
    assert b"Invalid email address" in response.data