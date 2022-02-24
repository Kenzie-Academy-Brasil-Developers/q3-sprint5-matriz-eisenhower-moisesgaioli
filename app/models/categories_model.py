from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


@dataclass
class Category(db.Model):

    __tablename__ = 'categories'

    id_category: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False, unique=True)
    description: str = Column(Text)

    

    tasks = relationship('Task', secondary='tasks_categories', backref='categories')