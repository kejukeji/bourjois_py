# coding: utf-8

from wtforms import BooleanField
import jsonpickle
import datetime
import time


from math import sin, asin, cos, radians, fabs, sqrt, degrees

pickler = jsonpickle.pickler.Pickler(unpicklable=False, max_depth=2)
EARTH_RADIUS=6371           # 地球平均半径，6371km

def flatten(model):
    """去除pickler.flatten里面的一个字段"""
    json = pickler.flatten(model)
    json.pop('_sa_instance_state', None)
    return json


def form_to_dict(form):
    form_dict = {}

    for key in form._fields:  # 可以编写一个更好的函数，可惜我不会。。。
        if isinstance(form._fields[key].data, BooleanField) or isinstance(form._fields[key].data, int):
            form_dict[key] = form._fields[key].data
            continue

        if form._fields[key].data:
            form_dict[key] = form._fields[key].data

    return form_dict


def time_diff(dt):
    dt = datetime.datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S")
    today = datetime.datetime.today()
    s = int((today - dt).total_seconds())

    # day_diff > 365, use year
    if s / 3600 / 24 >= 365:
        return str(s / 3600 / 24 / 365) + " 年前"
    elif s / 3600 / 24 >= 30:  # day_diff > 30, use month
        return str(s / 3600 / 24 / 30) + " 个月前"
    elif s / 3600 >= 24:  # hour_diff > 24, use day
        return str(s / 3600 / 24) + " 天前"
    elif s / 60 > 60:  # minite_diff > 60, use hour
        return str(s / 3600) + " 小时前"
    elif s > 60:  # second_diff > 60, use minite
        return str(s / 60) + " 分钟前"
    else:  # use "just now"
        return "刚刚"


def page_utils(count, page, per_page=10):
    min = 1
    max = count / per_page if count % per_page == 0 else count / per_page + 1
    page = page if ( page >= min and page <= max  ) else 1

    return page, per_page, max


#取得一个正确的返回字典
class success_dic(object):
    def __init__(self):
        self.dic = {}
        self.dic['status'] = 0
        self.dic['message'] = 'success'
        #self.dic['test'] = 'test success'

    def set(self, k, v):
        self.dic[k] = v


#取得一个错误的返回字典
class fail_dic(object):
    def __init__(self):
        self.dic = {}
        self.dic['status'] = 1
        self.dic['message'] = '没有查询到相应数据！'
        #self.dic['test'] = 'test fail'

    def set(self, k, v):
        self.dic[k] = v


def time_to_str(time):
    """

    """
    return time.strftime("%Y-%m-%d %H:%M:%S")


#把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d-%H")


def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False

def max_page(page, max, resp_suc):
    if max == 0:
        return False
    if int(page) > max:
        resp_suc['status'] = 1
        prompt = ['最多只有', str(max), '页']
        resp_suc['message'] = ''.join(prompt)
        return True
    else:
        return False

