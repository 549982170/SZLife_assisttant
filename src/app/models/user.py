# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月14日
@author: yizhiwu
用户类
'''
import logging

from flask_login import UserMixin

from app.db.memmode import tb_users


logger = logging.getLogger()


class User(UserMixin):

    def __init__(self, uid):
        self.uid = uid

    @property
    def id(self):
        return self.uid

    @property
    def obj(self):
        return tb_users.getObj(long(self.uid)) if tb_users.getObj(long(self.uid)) else {}

    @property
    def IsCanLogin(self):
        """判断是否能登录"""
        return True