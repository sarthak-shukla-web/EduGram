from datetime import datetime

from ..extensions import db


class Roadmap(db.Model):
    __tablename__ = "roadmaps"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    roadmap_topics = db.relationship(
        "RoadmapTopic",
        backref="roadmap",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }


class RoadmapTopic(db.Model):
    __tablename__ = "roadmap_topics"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    roadmap_id = db.Column(
        db.Integer,
        db.ForeignKey("roadmaps.id"),
        nullable=False
    )

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

    sequence = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="not_started",
        nullable=False
    )

    topic = db.relationship(
        "Topic",
        backref="roadmap_links"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "roadmap_id": self.roadmap_id,
            "topic_id": self.topic_id,
            "sequence": self.sequence,
            "status": self.status
        }