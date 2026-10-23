from datetime import datetime

from ..extensions import db


class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="not_started",
        nullable=False
    )

    completion_percentage = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    last_accessed = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    topic = db.relationship(
        "Topic",
        backref="progress_records"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "topic_id": self.topic_id,
            "status": self.status,
            "completion_percentage": self.completion_percentage,
            "last_accessed": (
                self.last_accessed.isoformat()
                if self.last_accessed
                else None
            )
        }