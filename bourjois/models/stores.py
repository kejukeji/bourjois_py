# coding: UTF-8

from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .area import Area

STORES = 'stores'

class Stores(Base, InitUpdate):
    '''门店'''
    __tablename__ = STORES
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(150), nullable=False)
    longitude = Column(Float(presicion=8), nullable=False)
    latitude = Column(Float(presicion=8), nullable=False)
    intro = Column(String(400), nullable=True)
    mall = Column(String(100), nullable=False)
    tel = Column(String(20), nullable=False)
    belong_area_id = Column(Integer, ForeignKey(Area.id, ondelete='cascade', onupdate='cascade'))
    base_path = Column(String(200), nullable=False)
    rel_path = Column(String(200), nullable=False)
    picture_name = Column(String(200), nullable=False)

    def __init__(self, **kwargs):
        '''初始化'''
        args = ('name', 'address', 'longitude', 'latitude', 'intro', 'mall', 'tel', 'belong_area_id','base_path', 'rel_path', 'picture_name')
        self.init_value(args, kwargs)

