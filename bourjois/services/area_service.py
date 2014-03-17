#coding : UTF-8

from bourjois.models.area import Area as Area
from bourjois.models.database import *

def get_id_by_city(city):
    city = city.decode('utf-8')[0:2].encode('utf-8')
    area = Area.query.filter(Area.name.like('%'+city+'%')).first()
    return area.id
