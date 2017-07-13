# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月9日
@author: yizhiwu
'''
import json
from subprocess import Popen

from app.db.dbentrust.dbpool import DBPool
from app.share.constants import configFilePath
from app.share.util import md5


configfiles = json.load(open(configFilePath, 'r'))
dbpool = DBPool()
dbpool.initPool(configfiles['db'])


def exportPacket():
    """导出依赖包到requestments.txt"""
    com = "pip freeze > requestments.txt" 
    p = Popen(com, shell=True)
    output = p.wait()
    if output == 0:  # 执行成功
        print 'exportPacket success'
    else:
        print 'exportPacket faild'
    
    
def instalPacket():
    """安装所需的包"""
    com = "pip install -d pgk/ -r requestments.txt"
    p = Popen(com, shell=True)
    output = p.wait()
    if output == 0:  # 执行成功
        print 'instalPacket success'
    else:
        print 'instalPacket faild'

def instalAllPacket():
    """安装所有的包"""
    com = "pip install -d pgk/ -r requestments.txt"
    p = Popen(com, shell=True)
    output = p.wait()
    if output == 0:  # 执行成功
        print 'instalAllPacket success'
    else:
        print 'instalAllPacket faild'

def setAcuserPwd(newpwd="123456"):
    sql = "select Id, AccountId from ac_users"
    result = dbpool.querySql(sql, True)
    for ca in result:
        Id = ca['Id']
        AccountId = ca['AccountId']
        sign = md5(AccountId+newpwd)
        sql = "update ac_users set AccountPassword='%s' where Id=%s" % (sign, Id)
        dbpool.execSql(sql)
        
if __name__ == '__main__':
    pass
    
    