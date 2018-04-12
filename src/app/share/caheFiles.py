# coding:utf-8
# !/user/bin/python
'''
Created on 2018年4月12日
@author: yizhiwu
内存缓存对象
'''
CACHE = {}  # 函数值缓存
LOCK_DICT = {}  # 线程池字典