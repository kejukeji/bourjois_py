# coding: UTF-8
from sqlalchemy import or_
from bourjois.models.stores import Stores as Stores
from bourjois.models.database import *

def find_by_city(city_id):
    stores_count = Stores.query.filter(Stores.belong_area_id==city_id).count()
    if stores_count == 1:
        stores = Stores.query.filter(Stores.belong_area_id==city_id).first()
    elif stores_count > 1:
        stores = Stores.query.filter(Stores.belong_area_id==city_id).all()
    else:
        stores = None
    return stores


def find_by_city_count(city_id):
    stores_count = Stores.query.filter(Stores.belong_area_id==city_id).count()
    return stores_count

def get_result_by_case(case):
    s = '%'+case+'%'
    stores_count = Stores.query.filter(or_(Stores.name.like(s),Stores.address.like(s))).count()
    stores = Stores.query.filter(or_(Stores.name.like(s),Stores.address.like(s)))


