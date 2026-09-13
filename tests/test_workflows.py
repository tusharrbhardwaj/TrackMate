from datetime import datetime
from io import BytesIO
from pathlib import Path

from app import db
from app.models.friendship import Friendship
from app.models.goal import Goal
from app.models.proof import Proof
from app.models.task import Task
from app.models.user import User


def register_and_login(client, username):
    email = f"{username}@example.com"
    client.post("/register", data={"username": username, "email": email, "password": "password123", "confirm_password": "password123"})
    client.post("/login", data={"email": email, "password": "password123"})


def create_goal(client, title="Finish project"):
    client.post("/goals/create", data={"title": title, "description": "Test"})


def get_user(app, username):
    with app.app_context():
        return db.session.execute(db.select(User).where(User.username == username)).scalar_one()


def get_goal(app, title="Finish project"):
    with app.app_context():
        return db.session.execute(db.select(Goal).where(Goal.title == title)).scalar_one()


def create_task(client, goal_id, weight=100, title="Complete task"):
    return client.post(
        f"/tasks/create/{goal_id}",
        data={"title": title, "description": "Test task", "deadline": "2026-12-31T12:00", "weight": str(weight)},
    )


def get_task(app, goal_id):
    with app.app_context():
        return db.session.execute(db.select(Task).where(Task.goal_id == goal_id)).scalar_one()


def submit_proof(client, task_id, words=100, filename="proof.png"):
    return client.post(
        f"/proof/submit/{task_id}",
        data={"description": " ".join(["done"] * words), "photo": (BytesIO(b"image"), filename)},
        content_type="multipart/form-data",
    )


def make_supervised_pending_proof(app):
    owner_client = app.test_client()
    supervisor_client = app.test_client()
    register_and_login(owner_client, "owner")
    register_and_login(supervisor_client, "supervisor")
    create_goal(owner_client)
    owner = get_user(app, "owner")
    supervisor = get_user(app, "supervisor")
    goal = get_goal(app)
    owner_client.post(f"/friends/send/{supervisor.id}")
    with app.app_context():
        friendship = db.session.execute(db.select(Friendship)).scalar_one()
    supervisor_client.post(f"/friends/accept/{friendship.id}")
    owner_client.post(f"/goals/{goal.id}/supervisor/{supervisor.id}")
    create_task(owner_client, goal.id)
    task = get_task(app, goal.id)
    submit_proof(owner_client, task.id)
    with app.app_context():
        proof = db.session.execute(db.select(Proof)).scalar_one()
    return owner_client, supervisor_client, owner, goal, task, proof


def test_task_weight_and_total_allocation_boundaries(client, app):
    register_and_login(client, "allocationowner")
    create_goal(client, "Allocation goal")
    goal = get_goal(app, "Allocation goal")
    assert create_task(client, goal.id, weight=0).status_code == 200
    assert create_task(client, goal.id, weight=1, title="One").status_code == 302
    assert create_task(client, goal.id, weight=99, title="Ninety nine").status_code == 302
    assert create_task(client, goal.id, weight=1, title="Over total").status_code == 200
    create_goal(client, "Maximum task")
    assert create_task(client, get_goal(app, "Maximum task").id, weight=100).status_code == 302
    create_goal(client, "Invalid task")
    assert create_task(client, get_goal(app, "Invalid task").id, weight=101).status_code == 200


def test_proof_input_boundaries_and_file_validation(client, app):
    register_and_login(client, "proofowner")
    for title, words, accepted in [("Ninety nine", 99, False), ("Exactly one hundred", 100, True), ("More than one hundred", 101, True)]:
        create_goal(client, title)
        goal = get_goal(app, title)
        create_task(client, goal.id)
        response = submit_proof(client, get_task(app, goal.id).id, words=words)
        assert (response.status_code == 302) is accepted
    create_goal(client, "Invalid image")
    goal = get_goal(app, "Invalid image")
    create_task(client, goal.id)
    assert b"Only JPG, JPEG and PNG images are allowed." in submit_proof(client, get_task(app, goal.id).id, filename="proof.gif").data


def test_unauthorized_user_cannot_view_goal(app):
    owner_client = app.test_client()
    other_client = app.test_client()
    register_and_login(owner_client, "goalowner")
    create_goal(owner_client, "Private goal")
    register_and_login(other_client, "outsider")
    assert other_client.get(f"/goals/{get_goal(app, 'Private goal').id}").status_code == 403


def test_accepted_friendship_cannot_be_rejected_as_pending(app):
    sender_client = app.test_client()
    receiver_client = app.test_client()
    register_and_login(sender_client, "sender")
    register_and_login(receiver_client, "receiver")
    sender_client.post(f"/friends/send/{get_user(app, 'receiver').id}")
    with app.app_context():
        friendship = db.session.execute(db.select(Friendship)).scalar_one()
    receiver_client.post(f"/friends/accept/{friendship.id}")
    assert receiver_client.post(f"/friends/reject/{friendship.id}").status_code == 400
    with app.app_context():
        assert db.session.get(Friendship, friendship.id).status == "ACCEPTED"


def test_proof_review_authorization_and_approval_workflow(app):
    _, supervisor_client, owner, _, task, proof = make_supervised_pending_proof(app)
    stranger_client = app.test_client()
    register_and_login(stranger_client, "stranger")
    assert stranger_client.post(f"/proof/approve/{proof.id}").status_code == 403
    assert supervisor_client.post(f"/proof/approve/{proof.id}").status_code == 302
    with app.app_context():
        assert db.session.get(Proof, proof.id).status == "APPROVED"
        assert db.session.get(Task, task.id).status == "COMPLETED"
        assert db.session.get(User, owner.id).rating == 1


def test_supervisor_rejection_reactivates_task_and_decreases_rating(app):
    _, supervisor_client, owner, _, task, proof = make_supervised_pending_proof(app)
    assert supervisor_client.post(f"/proof/reject/{proof.id}").status_code == 302
    with app.app_context():
        assert db.session.get(Proof, proof.id).status == "REJECTED"
        assert db.session.get(Task, task.id).status == "ACTIVE"
        assert db.session.get(User, owner.id).rating == -1


def test_completed_task_cannot_receive_another_proof(app):
    owner_client, supervisor_client, _, _, task, proof = make_supervised_pending_proof(app)
    assert submit_proof(owner_client, task.id, words=100).status_code == 302
    supervisor_client.post(f"/proof/approve/{proof.id}")
    assert submit_proof(owner_client, task.id, words=100).status_code == 302
    with app.app_context():
        assert db.session.get(Task, task.id).status == "COMPLETED"
        assert len(db.session.execute(db.select(Proof)).scalars().all()) == 1


def test_deleting_goal_removes_local_proof_file(client, app):
    register_and_login(client, "deleteowner")
    create_goal(client, "Delete goal")
    goal = get_goal(app, "Delete goal")
    proof_file = Path(app.config["PROOF_UPLOAD_FOLDER"]) / "delete-proof.png"
    proof_file.write_bytes(b"image")
    with app.app_context():
        task = Task(goal_id=goal.id, title="Task", deadline=datetime(2026, 12, 31), weight=100)
        db.session.add(task)
        db.session.flush()
        db.session.add(Proof(task_id=task.id, user_id=get_user(app, "deleteowner").id, description="proof", photo_path="uploads/proofs/delete-proof.png"))
        db.session.commit()
    assert client.post(f"/goals/{goal.id}/delete").status_code == 302
    assert not proof_file.exists()
