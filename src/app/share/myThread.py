# coding:utf-8
# !/user/bin/python
'''
Created on 2017年11月25日
@author: 线程类
'''
import hashlib
import pickle
import threading

from flask import request

from app.share.caheFiles import LOCK_DICT


class MyThread(threading.Thread):

    def __init__(self, func, args=None, kwargs=None):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        sign = request.url if hasattr(request, "endpoint") else None
        self.key = hashlib.sha1(pickle.dumps((self.func.func_name, sign))).hexdigest()
        self.result = None

    @property
    def lock(self):
        lock = LOCK_DICT.get(self.key)
        if not lock:
            lock = threading.RLock()
            LOCK_DICT[self.key] = lock
        return lock

    def run(self):
        """"重写start方法,加锁,逻辑处理异常抛出异常,这里可以拓展结果返回"""
        try:
            if self.lock.acquire():
                self.result = self.func(*self.args)
        except:
            raise
        finally:
            self.lock.release()

    def get_result(self):
        try:
            return self.result  # 获取时候需要join(), 不然主线程比子线程跑的快,会拿不到结果
        except:
            raise
