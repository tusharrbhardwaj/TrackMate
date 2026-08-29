from datetime import datetime, timezone
from app import db


class Friendship(db.Model):
    __tablename__ = "friendships"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
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


    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        backref="sent_friend_requests"
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        backref="received_friend_requests"
    )