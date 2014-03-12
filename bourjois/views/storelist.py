# coding: UTF-8
from flask import render_template,request
from bourjois.services.stores_service import *
from bourjois.services.area_service import *
from bourjois.utils.get_distance import *

def get_stores_list(city,latitude,longitude):
    city_id = get_id_by_city(city)
    stores_count = find_by_city_count(city_id)
    if latitude == 0 or latitude == None:
            store = find_by_city(city_id)
            return render_template('storelist.html',
                                   stores_count=stores_count,
                                   store=store)
    else:
        if stores_count == 1:
            store = find_by_city(city_id)
            store.distance = get_distance(store.latitude,store.longitude,latitude,longitude)
            return  render_template('storelist.html',
                            store=store)
        elif stores_count > 1:
            storeList = find_by_city(city_id)
            for stores in storeList:
                stores.distance = get_distance(stores.latitude,stores.longitude,latitude,longitude)
            store = sorted(storeList.items(),key=lambda distance:distance[1])
            return render_template('storelist.html',
                                   store=store,
                                   stores_count=stores_count)
        else:
            return ''

def find_by_case(case):
    stores = get_result_by_case(case)
    return stores

def goto_storelist():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')


def get_city_by_position(lat,lng):
    