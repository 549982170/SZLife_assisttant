# coding:utf-8
# !/user/bin/python
'''
Created on 2017年9月8日
@author: yizhiwu
'''


class Singleton(type):
    """Singleton Metaclass"""

    def __init__(self, name, bases, dic):
        super(Singleton, self).__init__(name, bases, dic)
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance


class UserManager:
    '''在线用户单例管理器'''

    __metaclass__ = Singleton

    def __init__(self):
        '''初始化单例管理器'''
        self._users = {}

    def addUser(self, userhandle):
        '''添加一个在线用户'''

        if userhandle.userId not in self._users.keys():
            self._users[userhandle.userId] = userhandle

    def getUserByID(self, userId):
        '''根据角色id获取用户实例
        @id （int） 用户id
        '''
        return self._users.get(userId)

    def dropUser(self, userhandle):
        '''移除在线用户
        @player （PlayerCharacter）角色实例
        '''
        try:
            del self._users[userhandle.userId]
        except:
            pass
