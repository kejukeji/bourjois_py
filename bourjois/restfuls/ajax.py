# coding: UTF-8

from flask.ext import restful
from bourjois.models.area import *

class GetArea(restful.Resource):
    '''获取区域'''
    @staticmethod
    def get():
        area = Area.query.filter().all()
        json = []
        for i in range(len(area)):
            json.append([area[i].id, area[i].name])

        return json