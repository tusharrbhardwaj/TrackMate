# Tests set up file

import pytest;
from app import create_app, db;

@pytest.fixture
def app(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                f"sqlite:///{(tmp_path / 'test.db').as_posix()}"
            ),
            "WTF_CSRF_ENABLED": False,
            "PROOF_UPLOAD_FOLDER": str(tmp_path / "proofs"),
        }
    )
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
