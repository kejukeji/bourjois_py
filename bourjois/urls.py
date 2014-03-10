# coding: UTF-8

from bourjois import app
from flask.ext import restful
from bourjois.views.index import index



#定义访问control路径


api = restful.Api(app)

#定义接口路劲


# 手机页面
app.add_url_rule('/index','index',index)