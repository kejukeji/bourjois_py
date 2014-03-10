# coding: UTF-8

from .database import Base
from sqlalchemy import Column, Integer, String
from .base_class import InitUpdate

AREA = 'area'

class Area(Base,InitUpdate):
    '''区域'''
    __tablename__ = AREA
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    def __init__(self, **kwargs):
        '''初始化'''
        self.init_value(('name'), kwargs)
