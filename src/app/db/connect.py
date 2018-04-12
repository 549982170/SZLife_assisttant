# coding:utf-8
# !/user/bin/python
'''
Created on 2018年4月12日
@author: yizhiwu
备注数据库连接
'''
import json

from app.share.constants import configFilePath
from app.db.dbentrust.dbpool import dbpool
from app.db.dbentrust.rdsclient import initRedis
from app.db.dbentrust.memclient import mclient
from app.db.dbadmin import load_admin_data


class Config(object):

    def __init__(self):
        self.cfg = json.load(open(configFilePath, 'r'))


class MysqlConnect(Config):

    def connect(self):
        """mysql连接"""
        dbpool.initPool(self.cfg['db'])


class RedisConnect(Config):

    def connect(self):
        """redis连接"""
        initRedis(self.cfg['redis']['host'], self.cfg['redis']['port'], self.cfg['redis']['password'], self.cfg['redis']['db'])


class MemcacheConnect(Config):

    def connect(self):
        """memcahce连接"""
        mclient.connect(self.cfg['memcached']['urls'], self.cfg['memcached']['hostname'])

#---数据库连接------
db_connect = MysqlConnect()
db_connect.connect()
redis_connect = RedisConnect()
redis_connect.connect()
memcache_connect = MemcacheConnect()
memcache_connect.connect()


def load_config_data():
    load_admin_data()

load_config_data()
