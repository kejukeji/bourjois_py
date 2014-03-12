# coding: UTF-8

import urllib2
import json


import xml.sax
import xml.sax.handler

class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping



if __name__ == '__main__':
    longitude = '121.473704' # 经度
    latitude = '31.230393' # 纬度
    get_address_url = 'http://api.map.baidu.com/geocoder?location=%s,%s' % (latitude, longitude)
    f = urllib2.urlopen(get_address_url)
    json_string = f.read()
    xh = XMLHandler()
    xml.sax.parseString(json_string, xh)
    ret = xh.getDict()
    print ret['province']
