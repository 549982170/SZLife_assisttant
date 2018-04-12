# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月8日
@author: yizhiwu
启动&配置文件
'''
from datetime import timedelta
from inspect import getmembers, isfunction
import json
import logging
import os
import threading
import traceback

from flask import Flask, session, request, redirect, g, render_template
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect, CSRFError

from app.db.connect import load_config_data
from app.db.syncdata import timerGetData
from app.handlers.core.usermanager import UserManager
from app.handlers.core.user.userbase import UserHandle
from app.models.adminuser import adminUser
from app.models.guestuser import Anonymous
from app.models.user import User
from app.share import jinja_filters
from app.share.constants import configFilePath, defaultStaticFolder, defaultTemplateFolder
from app.share.sooviiLogin import mysooviilogin, adminsooviilogin
from app.share.util import loggerJsonInfo


logger = logging.getLogger()

# 配置文件
configfiles = json.load(open(configFilePath, 'r'))
# ------flask配置-------------
app = Flask(__name__)
app.static_folder = os.path.join(defaultStaticFolder)
app.template_folder = os.path.join(defaultTemplateFolder)
app.config.from_object('config.config.Config')  # 配置类
# --------jinjia2配置----------
my_filters = {name: function for name, function in getmembers(jinja_filters) if isfunction(function)}
app.jinja_env.trim_blocks = True  # 去掉Jinja2语句内占据的空行
app.jinja_env.lstrip_blocks = True
app.jinja_env.filters.update(my_filters)  # 加载自定义过滤器函数ß
# -----flaskLogin插件---------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
# -------开启CSRF保护----------
csrf = CSRFProtect()
csrf.init_app(app)
# ------连接数据库,装载内存------------
load_config_data()
# ------启动定时扫描------------
timerGetData()
# --------用户登录初始化--------
# 连接缓存后导入用户类
mysooviilogin.init_login()
adminsooviilogin.init_login()
# --------用户登录初始化结束-------


@app.before_request
def before_request():
    """所有请求前执行方法"""
    try:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(seconds=configfiles['sessionMinutes'])
        login_manager.remember_cookie_duration = timedelta(days=configfiles['remember_cookie_day'])
        g.user = current_user
        msg = request.form.to_dict()
        if msg:
            t = threading.Thread(target=loggerJsonInfo, args=(msg,))  # 新线程执行请求日志写入,避免阻塞
            t.start()
    except:
        logger.error(traceback.format_exc())


@login_manager.unauthorized_handler  # 自定义未登录跳转
def unauthorized():
    return redirect(current_user.loginurl)


def register_blueprints(app):
    from app.myapp import register_blue
    register_blue(app)


register_blueprints(app)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):  # 尚未通过csrf验证
    try:
        logger.info(e)
        if request.is_xhr:  # 来自JavaScript XMLHttpRequest的触发, 则返回True
            return json.dumps({'status': 1, 'result': 0, "data": e.description, "msg": e.description})
        else:
            return render_template('csrf_error.html', reason=e.description), 400
    except Exception as e:
        logger.exception(e)
        return json.dumps({'status': 0, 'result': 0, "data": e.description, "msg": u"服务器异常"})


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.teardown_request
def after_request(error):
    if error is not None:  # 异常时候打印异常日志
        logger.error(traceback.format_exc())


@login_manager.user_loader  # 重新装载user对象
def load_user(userId):
    userId = "1"  # 测试
    if not userId.isdigit():
        return None
    urlrootpath = request.path.split("/")[1]
    if urlrootpath == "admin":
        user = adminUser(userId)
    else:
        user = User(userId)
        if not UserManager().getUserByID(userId):
            userhandle = UserHandle(userId)
            UserManager().addUser(userhandle)
    return user if user.obj and user.IsCanLogin else None  # 找不到改用户返回空


def testapp():
    return app


if __name__ == '__main__':
    app.run(host=configfiles['host'], port=configfiles['port'], use_reloader=False, use_debugger=False,
            threaded=True)  # 使用 Aptana/Eclipse 来调试,需要把 use_debugger 和 user_reloader 都设置为 False
