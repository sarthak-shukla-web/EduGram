from ..extensions import db


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    material_id = db.Column(
        db.Integer,
        db.ForeignKey("materials.id"),
        nullable=False
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    difficulty = db.Column(
        db.String(50),
        default="beginner"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "material_id": self.material_id,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty
        }