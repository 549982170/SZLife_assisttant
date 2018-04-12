# coding:utf-8
#!/user/bin/python
'''
Created on 2017年3月1日
@author: yizhiwu
'''
import json
import logging
import traceback

from flask import redirect, Blueprint, current_app, url_for, request
from flask_login import current_user
from app.handlers.core.usermanager import UserManager
from app.share.jsonEncode import JsonDataEncode
from app.share.constants import defaultStaticFolder, defaultTemplateFolder
from app.share.exceptions import ApiException


logger = logging.getLogger()

mod = Blueprint('index', __name__, static_folder=defaultStaticFolder, template_folder=defaultTemplateFolder)


@mod.before_request
def before_request():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()  # 没有认证返回登录页


@mod.route('/')
def index():
    try:
        return "hello,world!"
    except ApiException, e:
        return redirect(e.url)
    except:
        logger.error(traceback.format_exc())
        return redirect(url_for("user.login"))


@mod.route('/api/test', methods=['GET'])
def test():
    """测试"""
    try:
        Id = request.args.get("id")
        user = UserManager().getUserByID(current_user.id)
        redata = user.userhanler.test(Id)
        redict = {}
        redict["redata"] = redata
        return json.dumps({'status': 1, 'result': 1, "data": redata, "msg": u"scuess"}, cls=JsonDataEncode)
    except ApiException, e:
        return json.dumps(e.toDict())
    except Exception as e:
        logger.exception(e)
        return json.dumps({'status': 0, 'result': 0, "data": '', "msg": u"接口错误"})
