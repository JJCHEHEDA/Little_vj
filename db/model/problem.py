#-*- coding:utf-8 -*-

import sys
sys.path.append('..')

from sqlalchemy import *
from sqlalchemy import *
#from sqlalchemy.ext.declarative import declarative_base
from db.base import Base

class Problem(Base):
    __tablename__='problem'

    pro_id = Column(String(50), primary_key=True)
    pro_title = Column(String(100), nullable=False)
    time_limit = Column(Integer, nullable=False,default=0)
    memory_limit = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=False, default='')
    input = Column(Text, nullable=False, default='')
    output = Column(Text, nullable=False,default='')
    sample_input = Column(Text, nullable=False, default="")
    sample_output = Column(Text, nullable=False, default="")
    hint = Column(Text, nullable=False, default="")
    source = Column(Text, nullable=False, default="")
