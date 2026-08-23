import pytest
from app import create_app, db
from app.models.user import User;


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# def test_successful_registration(client, app):
#     response = client.post(
#         "/register",
#         data={
#             "username": "sambo",
#             "email": "sambo@example.com",
#             "password": "thesambo123",
#             "confirm_password": "thesambo123",
#         },
#         follow_redirects=True
#     )

#     assert response.status_code == 200
#     assert b"Registration successful" in response.data

#     with app.app_context():
#         user = db.session.execute(
#             db.select(User).where(User.username == "sambo")
#         ).scalar_one_or_none()

#         assert user is not None
#         assert user.email == "sambo@example.com"
#         assert user.password_hash != "thesambo123"

# def test_invalid_email(client):
#     response = client.post(
#         "/register",
#         data={
#             "username": "sambo",
#             "email": "aleshasha",
#             "password": "password123",
#             "confirm_password": "password123",
#         }
#     )
#     assert response.status_code == 200
#     assert b"Invalid email address" in response.data


# def test_password_confirm(client):
#     response = client.post(
#         "/register",
#         data={
#             "username": "sambo",
#             "email": "sambo@example.com",
#             "password": "password123",
#             "confirm_password": "password1234",
#         }
#     )
#     assert response.status_code == 200
#     assert b"Password confirmation unsuccessful." in response.data


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
    assert b"TrackMate Dashboard" in response.data


def test_incorrect_password(client, app):

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
            "password": "idnkwhattowrite",
        },
        follow_redirects=True
    )
    assert b"Incorrect password." in response.data


def test_wrong_email(client):
    response = client.post(
        "/login",
        data={
            "email": "adcnaslcn@example.com",
            "password": "password123",
        },
        follow_redirects=True
    )
    assert b"Incorrect email or password." in response.data


def login_to_enter_home_page(client):
    response = client.get(
        "/dashboard",
        follow_redirects=True
    )
    assert b"Log In first!" in response.data