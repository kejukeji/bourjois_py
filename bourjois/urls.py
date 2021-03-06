# coding: UTF-8

from bourjois import app, db
from flask.ext import restful

from bourjois.views.index import index
from bourjois.views.storelist import *

from flask.ext.admin import Admin
from bourjois.views.admin_page.index import HomeView
from bourjois.views.admin_page.stroes import StoresView
from bourjois.restfuls.ajax import *
from bourjois.views.admin_page.admin_login import login_view, register_view





#定义访问control路径
app.add_url_rule('/login', 'login_view', login_view, methods=('GET', 'POST'))
app.add_url_rule('/register','login_register', register_view, methods=('GET','POST'))

api = restful.Api(app)

#定义接口路劲
api.add_resource(GetArea, '/restful/admin/area')

#定义后台管理路径
admin = Admin(name=u'Home', index_view=HomeView())
admin.init_app(app)

admin.add_view(StoresView(db, name=u'门店', endpoint='superuser', category=u"门店管理"))


# 手机页面

app.add_url_rule('/index','index',index)
app.add_url_rule('/to_storelist','to_store_list',to_store_list, methods=('GEt','POST'))
app.add_url_rule('/storelist','get_city_by_position',get_city_by_position,methods=['GET','POST'])
app.add_url_rule('/citystorelist','get_cityStoreList',get_cityStoreList,methods=['GET','POST'])

