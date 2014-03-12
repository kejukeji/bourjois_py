#coding : UTF-8

from bourjois.models.area import Area as Area
from bourjois.models.database import *

def get_id_by_city(city):
    area = Area.query.filter(Area.name == city).first()
    return area.id
