from sqlalchemy.sql import func
from project import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key = True \
                            , autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    done = db.Column(db.Boolean, default = False)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done
        }