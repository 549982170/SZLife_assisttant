# coding:utf-8
#!/user/bin/python
'''
Created on 2017年4月13日
@author: yizhiwu
停服前执行同步数据
'''
import json
import logging
from app.db.dbentrust.dbpool import dbpool
from app.db.dbentrust.memclient import mclient
from app.db.dbentrust.rdsclient import initRedis
from app.db.syncdata import timerGetData
from app.share.constants import configFilePath

logger = logging.getLogger()

# 配置文件
configfiles = json.load(open(configFilePath, 'r'))

# ------dbpool连接------------
dbpool.initPool(configfiles['db'])  # dbpool连接
#---------redis连接-----------
initRedis(configfiles['redis']['host'], configfiles['redis']['port'], configfiles['redis']['password'], configfiles['redis']['db'])
#-------Memcache连接-----------
mclient.connect(configfiles['memcached']['urls'], configfiles['memcached']['hostname'])  # memcache连接
timerGetData(Time=1)