# coding: UTF-8
from bourjois.models.database import db

class BaseService():
    '''封装相同的操作'''
    def insert_model(self, model):
        '''插入一条数据'''