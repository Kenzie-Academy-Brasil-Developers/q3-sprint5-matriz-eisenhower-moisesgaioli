from collections import UserList
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref


@dataclass
class Eisenhower(db.Model):

    __tablename__ = 'eisenhowers'

    id_eisenhower: int = Column(Integer, primary_key=True)
    type_eisenhower: str = Column(String(100))
    


    tasks = relationship('Task', backref=backref('eisenhower', uselist=False))
