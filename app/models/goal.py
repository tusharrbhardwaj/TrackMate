from datetime import datetime, timezone
from app import db


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    supervisor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
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

    # IMPORTANT:
    # because Goal now has TWO foreign keys pointing to User,
    # we must explicitly tell SQLAlchemy which FK each relationship uses.

    owner = db.relationship(
        "User",
        foreign_keys=[owner_id],
        backref="goals"
    )

    supervisor = db.relationship(
        "User",
        foreign_keys=[supervisor_id],
        backref="supervised_goals"
    )