# coding:utf-8
#!/user/bin/python
'''
Created on 2017年5月31日
@author: yizhiwu
soovii登录用户信息接口验证模块,使用时直接引用mysooviilogin
'''
import base64
import logging
import traceback
import time
import requests

from app.db.dbadmin import get_syscfg_val
from app.share.constants import SOCP, GRANT_TYPE, GRANT_TYPE2


logger = logging.getLogger("adminlog") 

class mySooviiLogin(object):
    """用户验证类别"""
    
    def __init__(self):
        pass
    
    def init_login(self):
        self.serviceName = get_syscfg_val(15) + ":" + get_syscfg_val(6)   # 平台服务器域名
        self.ClientId = get_syscfg_val(19)      # 平台ID 企业中心提供
        self.ClientSecret = get_syscfg_val(20)  # 平台密码 企业中心提供
        self.HeaderValue = base64.b64encode((self.ClientId+":"+self.ClientSecret).encode("utf-8"))
        self.Authorization = "Basic" + " " + self.HeaderValue
        self.scope = SOCP
        self.grant_type = GRANT_TYPE
        self.grant_type2 = GRANT_TYPE2
        self.headers = {'Authorization': self.Authorization}
        self.tokenurl = self.serviceName + get_syscfg_val(3)  # 获取token的url
        self.loginUrl = self.serviceName + get_syscfg_val(18)  # 获取用户登录信息的url
        self.otherloginUrl = self.serviceName + get_syscfg_val(11)  # 获取其他用户登录信息的url
        self.allloginUrl = self.serviceName + get_syscfg_val(4)  # 获取所有用户登录信息的url
        self.resetinfo()
    
    def resetinfo(self):
        """重置信息"""
        self.refresh_token = u""
        self.tokenResult = {}
        self.loginResult = {}
        self.otherloginResult = {}
        self.logintime = 0

    def login(self, username, password):  # 登录用户
        try:
            payload = {
                "username": username,
                "password": password,
                "scope": self.scope,
                "grant_type": self.grant_type
            }
            r = requests.post(self.tokenurl, data=payload, headers=self.headers)
            result = r.json()
            if result.get("error"):  # 登录错误
                raise
            self.tokenResult = r.json()
            self.refresh_token = self.tokenResult.get("refresh_token")
            self.logintime = time.time()
        except:
            self.resetinfo()
            logger.error(traceback.format_exc())
        finally:
            return self.tokenResult
        
    
    def refreshToken(self):
        """刷新Token"""
        try:
            t1 = time.time()
            if t1 - self.logintime <= self.tokenResult.get("expires_in"):  # token尚未过期
                return self.tokenResult
            refresh_token = self.tokenResult.get("refresh_token")
            payload = {
                    "refresh_token": refresh_token,
                    "scope": self.scope,
                    "grant_type": self.grant_type2
                }
            r = requests.post(self.tokenurl, data=payload, headers=self.headers)
            self.tokenResult = r.json()
            self.token = self.tokenResult.get("refresh_token")
            self.logintime = t1
        except:
            self.resetinfo()
            logger.error(traceback.format_exc())
        finally:
            return self.tokenResult
    
    @property  
    def loginInfo(self):
        """获取自己的登录信息"""
        try:
            self.refreshToken()
            Authorization = self.tokenResult.get("token_type") + " " + self.tokenResult.get("access_token")
            headers = {'Authorization': Authorization}
            r = requests.get(self.loginUrl, headers=headers)
            self.loginResult = r.json()
            return self.loginResult
        except:
            self.resetinfo()
            logger.error(traceback.format_exc())
        finally:
            return self.loginResult
      
    def otherLoginInfo(self, userId):
        """获取其他用户信息"""
        try:
            self.refreshToken()
            Authorization = self.tokenResult.get("token_type") + " " + self.tokenResult.get("access_token")
            headers = {'Authorization': Authorization}
            otherloginUrl = self.otherloginUrl % userId
            r = requests.get(otherloginUrl, headers=headers)
            self.otherloginResult = r.json()
        except:
            self.resetinfo()
            logger.error(traceback.format_exc())
        finally:
            return self.otherloginResult
    
    @property  
    def allLoginInfo(self):
        """获取所有用户信息"""
        try:
            self.refreshToken()
            Authorization = self.tokenResult.get("token_type") + " " + self.tokenResult.get("access_token")
            headers = {'Authorization': Authorization}
            allloginUrl = self.allloginUrl
            r = requests.get(allloginUrl, headers=headers)
            self.allloginResult = r.json()
        except:
            self.resetinfo()
            logger.error(traceback.format_exc())
        finally:
            return self.allloginResult
    
    
    
class adminSooviiLogin(mySooviiLogin):
    """admin用户验证类别"""
    
    def __init__(self):
        super(adminSooviiLogin, self).__init__()
    
    def init_login(self):
        super(adminSooviiLogin, self).init_login()
        self.adminuser = get_syscfg_val(21)  # 默认admin用户帐号
        self.adminpwd = get_syscfg_val(22)  # 默认admin用户密码
    
    def login(self):
        super(adminSooviiLogin, self).login(self.adminuser, self.adminpwd)
      
    def refreshToken(self):
        """重写基类的刷新Token,使得adminSooviiLogin免登录"""
        try:
            if not self.tokenResult:
                self.login()
            t1 = time.time()
            if t1 - self.logintime <= self.tokenResult.get("expires_in"):  # token尚未过期
                return self.tokenResult
            refresh_token = self.tokenResult.get("refresh_token")
            payload = {
                    "refresh_token": refresh_token,
                    "scope": self.scope,
                    "grant_type": self.grant_type2
                }
            r = requests.post(self.tokenurl, data=payload, headers=self.headers)
            self.tokenResult = r.json()
            self.token = self.tokenResult.get("refresh_token")
            self.logintime = t1
        except:
            self.resetinfo()
            logger.error(traceback.format_exc())
        finally:
            return self.tokenResult
    
mysooviilogin = mySooviiLogin()

adminsooviilogin = adminSooviiLogin()
