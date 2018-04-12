# coding:utf-8
# !/user/bin/python
'''
Created on 2018年4月12日
@author: yizhiwu
备注:用户类
'''
import os
import uuid

from app.handlers.base_handler import Component
from app.db import memmode


class User(Component):
    '''人员模块'''

    def __init__(self, owner):
        Component.__init__(self, owner)
        self.obj = memmode.tb_users

    def test(self, Id):
        """测试跨模块"""
        test_other = self.owner.uploadhandler.test()
        return test_other + str(Id)
