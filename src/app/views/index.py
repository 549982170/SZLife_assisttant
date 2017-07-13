# coding:utf-8
#!/user/bin/python
'''
Created on 2017年3月1日
@author: yizhiwu
'''
import logging
import traceback 

from random import choice
from flask  import redirect, Blueprint, render_template, request, current_app, url_for
from flask_login import current_user, login_user
from app.db import memmode
from app.db.dbadmin import get_syscfg_val
from app.db.dbentrust.dbpool import dbpool
from app.models.user import User
from app.share.constants import defaultStaticFolder, defaultTemplateFolder
from app.share.exceptions import ApiException
from app.share.sooviiOauth import myoauth
from app.share.util import url_add_params, configfiles, forTipsMsgUrl, getLoginPageUrl

logger = logging.getLogger()
mod = Blueprint('index', __name__, static_folder=defaultStaticFolder, template_folder=defaultTemplateFolder)

# @mod.before_request
# def before_request():
#     if not current_user.is_authenticated:
#         return current_app.login_manager.unauthorized()  # 没有认证返回登录页

@mod.route('/')
def index():
    try:
        return "hello,world!"
    except ApiException, e:
        return redirect(e.url)
    except:
        logger.error(traceback.format_exc())
        return redirect(url_for("user.login"))



