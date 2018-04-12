# coding:utf-8
# !/user/bin/python
'''
Created on 2017年9月8日
@author: yizhiwu
'''

import weakref


class Component(object):
    '''
    抽象的组件对象
    '''

    def __init__(self, owner):
        '''
        创建一个组件
        @param owne: owner of this component
        '''
        self.owner = weakref.proxy(owner)



