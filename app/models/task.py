from app import db


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(
        db.Integer,
        db.ForeignKey("goals.id"),
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
    deadline = db.Column(
        db.DateTime,
        nullable=False
    )
    weight = db.Column(
        db.Integer,
        nullable=False
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default="ACTIVE"
    )
    deadline_changed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )
    goal = db.relationship(
        "Goal",
        backref="tasks"
    )