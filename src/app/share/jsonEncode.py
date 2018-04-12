# coding:utf-8
# !/user/bin/python
'''
Created on 2017年8月21日
@author: yizhiwu
处理json里面包含set对象
'''

from datetime import date
from datetime import datetime
import decimal
from json import JSONEncoder
import json
import pickle


class JsonDataEncode(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, set):
            return list(obj)
        else:
            return json.JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}
