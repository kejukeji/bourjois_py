# coding: UTF-8

from sqlalchemy import Column, Integer, String
from .database import Base
from .base_class import *

USER = 'user'

class User(Base, InitUpdate):
    '''用户'''
    __tablename__ = USER
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    password = Column(String(20), nullable=True)
    tel = Column(String(20), nullable=False)
    address = Column(String(100), nullable=True)


    def __init__(self, **kwargs):
        self.init_value(('name','password','tel','address'), kwargs)