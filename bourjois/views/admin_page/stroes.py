# coding: UTF-8

import logging
import os
import Image
from flask.ext.admin.contrib.sqla import ModelView
from flask import request, flash, redirect, url_for
from flask.ext import login
from flask.ext.admin.babel import gettext
from flask.ext.admin.base import expose
from flask.ext.admin.model.helpers import get_mdict_item_or_list
from flask.ext.admin.helpers import validate_form_on_submit
from flask.ext.admin.form import get_form_opts
from wtforms.fields import TextField, FileField, TextAreaField
from wtforms import validators
from werkzeug import secure_filename

from bourjois.utils.others import *
from bourjois.utils.ex_file import *
from bourjois.models.stores import *
from bourjois.var import *
from bourjois.models.user import *

log = logging.getLogger("flask-admin.sqla")

class StoresView(ModelView):
    '''门店view'''
    page_size = 20 # 每页显示条数
    can_create = True # 是否创建
    can_edit = True # 是否修改

    column_display_pk = True # 显示外键
    column_searchable_list = ('name', 'mall', 'address',) # 查询，根据model中的列名模糊查询吧
    column_exclude_list = ('longitude', 'latitude','base_path', 'rel_path', 'picture_name') # 过滤列名

    column_labels = dict(
        id = u'ID',
        name = u'门店名',
        address = u'地址',
        intro = u'介绍',
        mall = u'商城',
        belong_area_id = u'所属地区',
        tel = u'电话'
    )

    column_descriptions = dict(
        id = u'唯一标识',
        name = u'门店名',
        address = u'详细地址',
        intro = u'门店简单介绍',
        mall = u'所属商场',
        belong_area_id = u'所属区域',
        tel = u'电话号码'
    )

    form_overrides = dict(
        intro=TextAreaField
    )

    def scaffold_form(self):
        form_class = super(StoresView, self).scaffold_form()
        form_class.picture = FileField(label=u'门店图片', description=u'门店的图片')
        delattr(form_class, 'base_path')
        delattr(form_class, 'rel_path')
        delattr(form_class, 'picture_name')
        return form_class

    edit_template = 'admin/stores_edit.html'
    create_template = 'admin/stores_create.html'
    list_template = 'admin/stores_list.html'

    def __init__(self, db, **kwargs):
        super(StoresView, self).__init__(Stores, db, **kwargs)


    #def create_model(self, form):
    #    """改写flask的新建model的函数"""
    #
    #    try:
    #        pub_type_pictures = request.files.getlist("picture")  # 获取分类图片
    #        model = self.model(**form_to_dict(form))  # 更新pub_type的消息
    #        if not check_save_pub_type_pictures(pub_type_pictures, model):
    #            return False  # 保存图片， 同时更新model的路径消息
    #        self.session.add(model)  # 保存酒吧基本资料
    #        self.session.commit()
    #    except Exception, ex:
    #        flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
    #        logging.exception('Failed to create model')
    #        self.session.rollback()
    #        return False
    #    else:
    #        self.after_model_change(form, model, True)
    #
    #    return True

    def create_model(self, form):
        """添加酒吧和管理"""

        try:
            form_dict = form_to_dict(form)
            #if not self._valid_form(form_dict):
            #    flash(u'用户名重复了，换一个呗', 'error')
            #    return False
            picture = request.files.getlist('picture')
            stores = self._get_stores(form_dict)
            save_stores_pictures(stores, picture)
            self.session.add(stores)
            self.session.commit()

        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to create model')
            self.session.rollback()
            return False

        return True

    def update_model(self, form, model):
        """添加酒吧和管理"""

        try:
            #if not self._valid_form(form_dict):
            #    flash(u'用户名重复了，换一个呗', 'error')
            #    return False
            picture = request.files.getlist('picture')
            model.update(**form_to_dict(form))
            save_stores_pictures(model, picture)
            self.session.commit()

        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to create model')
            self.session.rollback()
            return False

        return True

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        return_url = request.args.get('url') or url_for('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        form = self.edit_form(obj=model)

        if validate_form_on_submit(form):
            if self.update_model(form, model):
                if '_continue_editing' in request.form:
                    flash(gettext('Model was successfully saved.'))
                    return redirect(request.full_path)
                else:
                    return redirect(return_url)

        # 改变小数点后面数字的个数
        form.latitude.places = 8
        form.longitude.places = 8

        return self.render(self.edit_template,
                           model=model,
                           form=form,
                           form_opts=get_form_opts(self),
                           form_rules=self._form_edit_rules,
                           return_url=return_url)

    #def is_accessible(self):  # 登陆管理功能先关闭，后期添加
    #    return current_user.is_admin()

    def _valid_form(self, form_dict):
        # 验证用户名是否重复
        if not self._has_user(form_dict['user']):
            return True

        return False

    def _has_user(self, user, model=None):
        """检查用户是否存在，不存在返回False"""
        if model is None:
            return bool(User.query.filter(User.name == user).count())
        else:
            return False

    def _get_user(self, form_dict, pub_id):
        """通过字典返回一个user类"""
        return User(name=form_dict['user'])

    def _get_stores(self, form_dict):
        """通过字典返回一个stores类"""
        return Stores(name=form_dict['name'],
                   intro=form_dict.get('intro', None),
                   address=form_dict.get('address'),
                   mall=form_dict.get('mall'),
                   tel=form_dict.get('tel', None),
                   belong_area_id=form_dict.get('belong_area_id'),
                   longitude=form_dict.get('longitude'),
                   latitude=form_dict.get('latitude'))


def save_stores_pictures(stores, pictures):
    """保存酒吧图片"""
    for picture in pictures:
        if not allowed_file_extension(picture.filename, STORES_PICTURE_ALLOWED_EXTENSION):
            continue
        else:
            upload_name = picture.filename
            base_path = STORES_PICTURE_BASE_PATH
            rel_path = STORES_PICTURE_REL_PATH
            pic_name = time_file_name(secure_filename(upload_name), sign='_')

            picture.save(os.path.join(base_path+rel_path+'/', pic_name))

            stores.base_path = base_path
            stores.rel_path = rel_path
            stores.picture_name = pic_name
            # save_thumbnail(stores, pic_name)


def save_thumbnail(stores, picture_name):
    """通过图片ID，查找图片，生产略缩图，存储本地，然后存储数据库"""
    save_path = stores.base_path + stores.rel_path + '/'
    picture = save_path + picture_name
    im = Image.open(picture)
    im.thumbnail((256, 256))
    im.save(save_path+picture_name, '.jpeg')