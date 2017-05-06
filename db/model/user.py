#-*- coding:utf-8 -*-

from sqlalchemy.orm import relationship
from sqlalchemy.types import *
from sqlalchemy.schema import Column
from db.base import Base
from db.model import submission

class User(Base):
    __tablename__ = "vj_user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(CHAR(32), nullable=False)

    vj_submission = relationship("Submission", back_populates="vj_user")


