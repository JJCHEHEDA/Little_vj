#-*- coding:utf-8 -*-

from sqlalchemy import * 
from sqlalchemy.orm import *

uri = 'mysql+mysqlconnector://root:jjcheheda@localhost/little_vj'
'''
engine = create_engine(uri)
Session = sessionmaker(bind=engine)
sql_session = Session()
Base.metadata.create_all(engine)
'''

engine = create_engine(uri, encoding='utf-8')
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
sql_session = Session()
