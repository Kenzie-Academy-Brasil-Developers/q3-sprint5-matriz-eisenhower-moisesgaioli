from unicodedata import category
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import validates

from app.exc.tasks_exc import ValidadeImportanceUrgency


@dataclass
class Task(db.Model):

    __tablename__ = 'tasks'


    id_task: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False, unique=True)
    description: str = Column(Text)
    duration: int = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)


    eisenhowers_id = Column(Integer, ForeignKey('eisenhowers.id_eisenhower'), nullable=False)



    @validates('importance', 'urgency')
    def validate_importance(self, key, value):

        if value != 1 and value != 2:
            raise ValidadeImportanceUrgency()

        return value