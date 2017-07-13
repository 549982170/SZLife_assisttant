# coding:utf-8
#!/user/bin/python
'''
Created on 2017年3月10日
@author: yizhiwu
OAuth登录
'''
import os
import base64
import json
import logging
from flask import current_app
from flask_oauthlib.client import OAuth
from flask_oauthlib.utils import to_bytes
from oauthlib.common import to_unicode
from oauthlib.oauth2 import LegacyApplicationClient
from app.db.dbadmin import get_syscfg_val

logger = logging.getLogger() 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # 服务器没有配置SSL

class myOAuth(OAuth):
    def __init__(self, app=None):
        super(myOAuth, self).__init__(app)
        self.app = app
        self.soovii = None
    
    def init_app(self, app):
        super(myOAuth, self).init_app(app)
        self.soovii = self.remote_app(
            'soovii',
            consumer_key=get_syscfg_val(1),  # 平台ID 企业中心提供
            consumer_secret=get_syscfg_val(2),  # 平台密码 企业中心提供
            request_token_params={},
            base_url=get_syscfg_val(15) + ":" + get_syscfg_val(6),  # 接口地址
            request_token_url=None,
            access_token_method='POST',
            access_token_url=get_syscfg_val(15) + ":" + get_syscfg_val(6) + get_syscfg_val(3),  # 登录接口url
            authorize_url=get_syscfg_val(15) + ":" + get_syscfg_val(6) + get_syscfg_val(7)  # 刷新token
        )
        
        self.api_client = LegacyApplicationClient(self.soovii.consumer_key)
        self.soovii.tokengetter(self.get_access_token)
    
    def get_access_token(self):
        if (not hasattr(current_app, "token")):
            client_credential = ("%s:%s" % (self.soovii.consumer_key, self.soovii.consumer_secret))
            headers = { "Authorization": "Basic " + to_unicode(base64.encodestring(to_bytes(client_credential))).replace("\n", "") }
            body = self.api_client.prepare_request_body(get_syscfg_val(8), get_syscfg_val(9))  # 对于网址类型的型的项目用户名密码，随意填写，如"soovii", "soovii"
    
            resp, content = self.soovii.http_request(
                self.soovii.access_token_url, headers, to_bytes(body), method="POST"
            )
            if resp.code not in (200, 201):
                logger.info('Invalid response')
            else:
                dic = json.loads(to_unicode(content))
                current_app.token = dic
                return dic
        else:
            return current_app.token
    
myoauth = myOAuth()


