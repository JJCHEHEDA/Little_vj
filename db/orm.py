#-*- coding:utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from db.model.problem import Problem
from db.model.user import User
from db.model.submission import Submission
from db.base import Base

class ProManagerORM():
    def __init__(self):
        uri = 'mysql+mysqlconnector://root:@localhost/jjc'
        self.engine = create_engine(uri)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def CreateNewPro(self, pro_info):
        self.session.execute(
                Problem.__table__.insert(),
                [{'pro_id':p['pro_id'],'pro_title':p['pro_title'],'time_limit':p['time_limit'],'memory_limit':p['memory_limit'],'description':p['description'],'input':p['input'],'output':p['output'],'sample_input':p['sample_input'],'sample_output':p['sample_output'],'source':p['source']}for p in pro_info]
        )
        self.session.commit()

    def GetAllPro(self):
        return self.session.query( Problem )

    def GetProById(self, num):
        return self.session.query( Problem ).filter(
                Problem.pro_id == num).one()

    def GetProList(self):
        return self.session.query( Problem ).order_by(Problem.pro_id).limit(50)

    def GetTiById(self, num):
        return self.session.query( Problem.pro_title ).filter(
                Problem.pro_id == num).one()


class UserManagerORM():
    def __init__(self):
        url = 'mysql+mysqlconnector://root:@localhost/jjc'
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def CreateNewUser(self, user_info): 
        self.session.execute(
                User.__table__.insert(),
                [{'username':u['username'], 'password':u['password']}for u in user_info]
        )
        self.session.commit()

    def If_Name(self, the_name):
        return self.session.query( User.password ).filter(
                User.username == the_name).one()

    def IdByInfo(self, the_info):
        return self.session.query( User.user_id ).filter(
                User.username == the_info["user"]).one()

    def InfoById(self, the_id):
        return self.session.query( User ).filter(
                User.user_id == the_id).one()


class SubManagerORM():
    def __init__(self):
        url = 'mysql+mysqlconnector://root:@localhost/jjc'
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def CreateNewSub(self, info):
        self.session.execute(
                Submission.__table__.insert(),
                [{'problem_id':i['Pro.ID'], 'judge_status':i['Judge Status'],'time_cost':i['Exe.Time'], 'memory_cost':i['Exe.Memory'],'code_language':i['Language'],'code_length':i['Code Len.'], 'submit_time':i['Submit Time'], 'auth_id':1}for i in info]
                )
        self.session.commit()

    def InfoAll(self):
        return self.session.query( Submission ).order_by(Submission.id).limit(50)






