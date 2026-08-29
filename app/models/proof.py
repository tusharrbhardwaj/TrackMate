from datetime import datetime, timezone;
from app import db;

class Proof(db.Model):
    __tablename__ = "proofs"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id"),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    description = db.Column(
        db.Text,
        nullable=False
    )
    photo_path = db.Column(
        db.String(255),
        nullable=False
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    task = db.relationship(
        "Task",
        backref="proofs"
    )
    user = db.relationship(
        "User",
        backref="proofs"
    )