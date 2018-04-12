# coding:utf-8
# !/user/bin/python
'''
Created on 2017年9月8日
@author: yizhiwu
'''
import logging

from app.db.memmode import tb_users
from app.handlers.files_handler.upload_handler import Upload
from app.handlers.user_handler.user_handler import User


logger = logging.getLogger()


class UserHandle(object):

    def __init__(self, userId):
        # ------不可变属性------------------
        self.userId = userId
        self.user_id = long(userId)

        # ------加载类------------------
        self.uploadhandler = Upload(self)
        self.userhanler = User(self)

    @property
    def data(self):
        return tb_users.getObjData(self.user_id)
