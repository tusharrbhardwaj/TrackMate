import pytest
from app import create_app, db
from app.models.user import User


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
    assert b"Registration successful" in response.data

    with app.app_context():
        user = db.session.execute(
            db.select(User).where(User.username == "sambo")
        ).scalar_one_or_none()

        assert user is not None
        assert user.email == "sambo@example.com"
        assert user.password_hash != "thesambo123"