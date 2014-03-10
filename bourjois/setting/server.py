# coding: utf-8

from bourjois.setting.secret import KJKJ_DB_NAME,KJKJ_DB_PASSWORD,KJKJ_DB_USER,KJKJ_SECRET_KEY_SERVER

# flask模块需要的配置参数
# ===============================================================
DEBUG = False  # 是否启动调试功能
SECRET_KEY = KJKJ_SECRET_KEY_SERVER  # session相关的密匙

# models模块需要的配置参数
# ===============================================================
SQLALCHEMY_DATABASE_URI = 'mysql://' + KJKJ_DB_USER + ':' + KJKJ_DB_PASSWORD + '@127.0.0.1:3306/' \
                          + KJKJ_DB_NAME + '?charset=utf8'  # 连接的数据库
SQLALCHEMY_ECHO = False  # 是否显示SQL语句