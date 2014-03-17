# coding: UTF-8
from flask import render_template,request, url_for, redirect
from bourjois.services.stores_service import *
from bourjois.services.area_service import *
from bourjois.utils.get_distance import *
from bourjois.utils.get_city import *

def get_stores_list(city,latitude,longitude,flag):
    if city:
        city_id = get_id_by_city(city)
    else:
        city_id = 1
    stores_count = find_by_city_count(city_id)
    if latitude == 0 or latitude == None:
            store = find_by_city(city_id)
            return render_template('storelist.html',
                                   stores_count=stores_count,
                                   store=store,
                                   flag=flag)
    else:
        if stores_count == 1:
            store = find_by_city(city_id)
            store.distance = get_distance(store.latitude,store.longitude,latitude,longitude)
            return  render_template('storelist.html',
                            store=store,
                            flag=flag)
        elif stores_count > 1:
            storeList = find_by_city(city_id)
            for stores in storeList:
                stores.distance = get_distance(stores.latitude,stores.longitude,latitude,longitude)
            store = sorted(storeList.items(),key=lambda distance:distance[1])
            return render_template('storelist.html',
                                   store=store,
                                   stores_count=stores_count,
                                   flag=flag)
        else:
            return ''

def to_store_list():
    '''to page'''
    return render_template('storelist.html',
                           markd='first')

def find_by_case(case):
    stores = get_result_by_case(case)
    return stores




def get_city_by_position():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    flag = request.args.get('flag')
    city = get_city(lat,lng)
    # city = None
    return get_stores_list(city,lat,lng,flag)

