# coding:utf-8
#!/user/bin/python
'''
Created on 2017年3月14日
@author: yizhiwu
匿名用户类
'''
from flask import url_for, request
from flask_login import AnonymousUserMixin


class Anonymous(AnonymousUserMixin):

    def __init__(self):
        self.username = 'Guest'

    @property
    def id(self):
        return 0

#     @property
#     def loginurl(self):
#         urlrootpath = request.path.split("/")[1]
#         if urlrootpath == "admin":
#             return url_for("adminuser.login")
#         else:
#             return url_for("user.login")

    @property
    def Data(self):
        return {}
