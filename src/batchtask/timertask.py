# coding:utf-8
#!/user/bin/python
'''
Created on 2017年7月10日
@author: yizhiwu
后端定时任务进程
'''
import datetime
import json
import logging
import socket
import time
import traceback

from dbentrust.dbpool import dbpool
from dbentrust.madminanager import MAdminManager
from dbentrust.memclient import mclient
from dbentrust.mmode import MAdmin

socket.setdefaulttimeout(10)  # 限制http超时时间(秒)
# ----------日志操作----------
logger = logging.getLogger()  # 获取dblog的日志配置
# ----------全局参数----------
CF_SYSCFG = {}
# ----------数据库连接----------
configfiles = json.load(open('../config/config.json', 'r'))
dbpool.initPool(configfiles['db'])  # 独立日志的dbpool连接
# ---------缓存连接与导入 -------
urls = configfiles['memcached']['urls']
hostname = configfiles['memcached']['hostname']
mclient.connect(urls, hostname)
# -------连接后注册内存对象 ------
# -------------------------------处理任务逻辑-----------------------------------------


def fun_1000(task):
    """剧本删除清理"""
    try:
        curdatetime = task['curdatetime']
        Intdate = task['Intdate']
        taskdatetime = task['taskdatetime']
        taskdate = task['taskdate']
        # 判断执行时间
        if taskdatetime.time() > curdatetime.time():  # 时间未到，跳过
            if Intdate != taskdate:  # 第二天,状态置0
                sql = "update tb_batchtask set taskdate=%s,status=0 where id=1000" % (Intdate)
                dbpool.execSql(sql)
            return

        sql = "update tb_batchtask set taskdate=%s,status=1 where id=1000" % (Intdate)
        dbpool.execSql(sql)
        logger.info("%s %s完成" % (Intdate, task['taskname']))
    except Exception as _ex:
        logger.error("%s %s异常" % (Intdate, task['taskname']))
        logger.error(traceback.format_exc())
        sql = "update tb_batchtask set taskdate=%s,status=2 where id=1000" % (Intdate)
        dbpool.execSql(sql)


def fun_1001(task):
    """文件清理"""
    try:
        curdatetime = task['curdatetime']
        Intdate = task['Intdate']
        taskdatetime = task['taskdatetime']
        taskdate = task['taskdate']
        # 判断执行时间
        if taskdatetime.time() > curdatetime.time():  # 时间未到，跳过
            if Intdate != taskdate:  # 第二天,状态置0
                sql = "update tb_batchtask set taskdate=%s,status=0 where id=1001" % (Intdate)
                dbpool.execSql(sql)
            return

        sql = "update tb_batchtask set taskdate=%s,status=1 where id=1001" % (Intdate)
        dbpool.execSql(sql)
        logger.info("%s %s完成" % (Intdate, task['taskname']))
    except Exception as _ex:
        logger.error("%s %s异常" % (Intdate, task['taskname']))
        logger.error(traceback.format_exc())
        sql = "update tb_batchtask set taskdate=%s,status=2 where id=1001" % (Intdate)
        dbpool.execSql(sql)

# -------------------------------处理定时任务-----------------------------------------
if __name__ == '__main__':
    logger.info('批量任务后台程序启动....')
    # --------------重新加载配置 --------------
    CF_SYSCFG.clear()
    queryResult = dbpool.querySql("select * from cf_syscfg", True)
    for ca in queryResult:
        CF_SYSCFG[ca['Id']] = ca['content']

    while True:
        try:
            # 执行日期
            curdatetime = datetime.datetime.now()
            Intdate = int(curdatetime.strftime("%Y%m%d"))
            # 查询未执行的一次性任务+以及当天未执行的每日任务+非当天的任务(status 0-待执行，1-执行成功，2-失败)
            sql = "select * from tb_batchtask where tasktype=1 or (tasktype=2 and ((taskdate=%s and status=0) or (taskdate<>%s) and status=1))" % (Intdate, Intdate)
            queryResult = dbpool.querySql(sql, True)
            for task in queryResult:
                task['curdatetime'] = curdatetime  # 现在的时间对象
                task['Intdate'] = Intdate  # 现在的时间日期
                task['taskdatetime'] = datetime.datetime.strptime(str("%s %s" % (task['taskdate'], task['starttime'])), '%Y%m%d %H:%M')  # 字符串转日期
                if task['id'] == 1000:  # 每日22：00 清理剧本删除后的相关数据
                    fun_1000(task)
                if task['id'] == 1001:  # 每日23：00 清理不存在的图片文件
                    fun_1001(task)

        except Exception as e:
            logger.error(traceback.format_exc())
        finally:
            time.sleep(10)
