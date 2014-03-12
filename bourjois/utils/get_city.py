#coding: UTF-8
import urllib2
from .ex_xml import *

def get_city(lat,lng):
    get_address_url = 'http://api.map.baidu.com/geocoder?location=%s,%s' % (lat, lng)
    f = urllib2.urlopen(get_address_url)
    json_string = f.read()
    xh = XMLHandler()
    xml.sax.parseString(json_string, xh)
    ret = xh.getDict()
    return ret['city'].encode('UTF-8')