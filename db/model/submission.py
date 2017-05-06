#-*- coding:utf-8 -*-

from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.types import *
from sqlalchemy.orm import relationship
from db.base import Base

class Submission(Base):
    __tablename__ = "vj_submission"

    id = Column(Integer, nullable=False, primary_key=True)
    auth_id = Column(Integer, ForeignKey('vj_user.user_id'))
    problem_id = Column(Integer, nullable=False)
    #submitter_id = Column(Integer, nullable=False)
    judge_status = Column(String(200), nullable=False, default="Submitting",
            server_default="Submitting")
    time_cost = Column(
            String(200), nullable=False, default=0, server_default=text('0'))
    memory_cost = Column(
            String(200), nullable=False, default=0, server_default=text('0'))
    #source_code = Column(Text, nullable=False)
    code_language = Column(String(20), nullable=False)
    code_length = Column(
            String(200), nullable=False, default=0, server_default=text('0'))
    submit_time = Column(DateTime, nullable=False,
            server_default=text("NOW()"))

    vj_user = relationship("User", back_populates="vj_submission")
