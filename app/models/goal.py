from datetime import datetime, timezone;
from app import db;

class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    description = db.Column(
        db.Text,
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    owner = db.relationship(
        "User",
        backref="goals"
    )