# coding:utf-8
# !/user/bin/python
'''
Created on 2018年4月12日
@author: yizhiwu
'''
import logging
import traceback

from flask import request, redirect, Blueprint, current_app, url_for
from flask_login import current_user, login_user, logout_user

from app.handlers.core import usermanager
from app.handlers.core.user.userbase import UserHandle
from app.models.adminuser import adminUser
from app.share.constants import admintemplateFolder, adminstaticFolder
from app.share.exceptions import ApiException


logger = logging.getLogger()

mod = Blueprint('adminuser', __name__, static_folder=admintemplateFolder, template_folder=adminstaticFolder)


@mod.before_request
def before_request():
    if not current_user.is_authenticated and request.path.split("/")[2] != "login":
        return current_app.login_manager.unauthorized()  # 没有认证返回登录页


@mod.route('/')
def index():
    try:
        return "hello,world!"
    except ApiException, e:
        return redirect(e.url)
    except:
        logger.error(traceback.format_exc())
        return redirect(url_for("adminuser.login"))


@mod.route('/login', methods=['GET', 'POST'])
def login():
    try:
        Id = "1"
        user = adminUser(Id)
        login_user(user, True)  # 记住登录状态
        return redirect(url_for("adminuser.index"))
    except ApiException, _e:
        pass
    except:
        logger.error(traceback.format_exc())
        pass


@mod.route('/logout')
def logout():
    # 如果会话中有用户名就删除它。
    userhandle = UserHandle(current_user.id)
    usermanager().dropUser(userhandle)
    logout_user()
    return redirect(current_user.loginurl)
