from datetime import datetime

from ..extensions import db


class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    file_type = db.Column(
        db.String(50),
        nullable=False
    )

    file_path = db.Column(
        db.String(500),
        nullable=False
    )

    processing_status = db.Column(
        db.String(50),
        default="pending",
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    topics = db.relationship(
        "Topic",
        backref="material",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "file_type": self.file_type,
            "processing_status": self.processing_status,
            "uploaded_at": (
                self.uploaded_at.isoformat()
                if self.uploaded_at
                else None
            )
        }