# coding: UTF-8

from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from .area import Area

STORES = 'stores'

class Stores(Base, InitUpdate):
    '''门店'''
    __tablename__ = STORES
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(150), nullable=False)
    intro = Column(String(400), nullable=True)
    mall = Column(String(100), nullable=False)
    tel = Column(String(20), nullable=False)
    belong_area_id = Column(Integer, nullable=False)
    base_path = Column(String(200), nullable=True)
    rel_path = Column(String(200), nullable=True)
    picture_name = Column(String(200), nullable=True)
    longitude = Column(DOUBLE, nullable=False)
    latitude = Column(DOUBLE, nullable=False)

    def __init__(self, **kwargs):
        '''初始化'''
        args = ('name', 'address','intro', 'mall', 'tel', 'belong_area_id', 'longitude', 'latitude')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        '''更新'''
        args = ('name', 'address','intro', 'mall', 'tel', 'belong_area_id', 'longitude', 'latitude')
        self.update_value(args, kwargs)

