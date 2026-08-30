from io import BytesIO
from app import db
from app.models.proof import Proof
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime;


def create_user_and_task(client, app):
    client.post(
        "/register",
        data={
            "username": "fen",
            "email": "fen@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
    )
    client.post(
        "/login",
        data={
            "email": "fen@example.com",
            "password": "password123",
        }
    )
    client.post(
        "/goals/create",
        data={
            "title": "Yoyo",
            "description": "Test goal for proof"
        }
    )
    with app.app_context():
        goal = db.session.execute(
            db.select(Goal).where(
                Goal.title == "Yoyo"
            )
        ).scalar_one()
        task = Task(
            goal_id=goal.id,
            title="Yoyo",
            description="Test task for proof",
            deadline=datetime(2026, 8, 30, 23, 0),   
            weight=100
        )

        db.session.add(task)
        db.session.commit()

        return task.id


# Successful proof submission
def test_submit_proof_success(client, app, monkeypatch):
    task_id = create_user_and_task(client, app)

    # Prevent real upload to Supabase
    def fake_upload(*args, **kwargs):
        return {"path": "test-image.png"}

    monkeypatch.setattr(
        "app.routes.proof.supabase.storage.from_",
        lambda bucket: type(
            "Storage",
            (),
            {"upload": fake_upload}
        )()
    )

    response = client.post(
        f"/proof/submit/{task_id}",
        data={
            "description": "I completed the task successfully ly ly",
            "photo": (
                BytesIO(b"fake image"),
                "test.png"
            )
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Proof submitted successfully." in response.data

    with app.app_context():
        proof = db.session.execute(
            db.select(Proof)
        ).scalar_one()

        assert proof.task_id == task_id
        assert proof.status == "PENDING"
        assert proof.description == "I completed the task successfully ly ly"


# Explanation cannot contain more than 100 words
def test_proof_description_too_long(client, app):
    task_id = create_user_and_task(client, app)
    long_description = " ".join(
        ["word"] * 101
    )

    response = client.post(
        f"/proof/submit/{task_id}",
        data={
            "description": long_description,
            "photo": (
                BytesIO(b"fake image"),
                "test.png"
            )
        },
        content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert b"Explanation cannot contain more than 100 words." in response.data


# Image is required
def test_proof_requires_image(client, app):
    task_id = create_user_and_task(client, app)
    response = client.post(
        f"/proof/submit/{task_id}",
        data={
            "description": "I completed the task."
        }
    )
    assert response.status_code == 200
    assert b"This field is required." in response.data


# User cannot submit another proof while one is pending
def test_cannot_submit_second_pending_proof(client, app, monkeypatch):
    task_id = create_user_and_task(client, app)
    def fake_upload(*args, **kwargs):
        return {"path": "test-image.png"}
    monkeypatch.setattr(
        "app.routes.proof.supabase.storage.from_",
        lambda bucket: type(
            "Storage",
            (),
            {"upload": fake_upload}
        )()
    )

    first_response = client.post(
        f"/proof/submit/{task_id}",
        data={
            "description": "First proof.",
            "photo": (
                BytesIO(b"fake image"),
                "test.png"
            )
        },
        content_type="multipart/form-data"
    )
    assert first_response.status_code == 302

    second_response = client.post(
        f"/proof/submit/{task_id}",
        data={
            "description": "Second proof.",
            "photo": (
                BytesIO(b"fake image"),
                "test2.png"
            )
        },
        content_type="multipart/form-data",
        follow_redirects=True
    )
    assert second_response.status_code == 200
    assert b"already have a proof waiting for review" in second_response.data