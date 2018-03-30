# coding:utf-8
#!/user/bin/python
'''
Created on 2017年3月22日
@author: yizhiwu
自动化脚本
'''

import re
import sys
import json
import os

from time import sleep
from time import strftime, localtime
from fabric.api import settings, run, local, cd

host = '111.230.177.230'
root = 'root'
appuser = 'appuser'

configfiles = json.load(open(os.path.join('config', 'config.json'), 'r'))

key_filename = "./id_rsa"

redis_port = configfiles["redis"]["port"]

memcahce_port = configfiles["memcached"]["urls"][0].split(":")[1]

hostname = configfiles["memcached"]["hostname"]


def getPid(portNo):
    output = run("netstat -anp|grep " + str(portNo) + "  |awk '{printf $7}'|cut -d/ -f1")
    pid = re.findall(r'\d+', output)[-1]
    return pid


def progress(percent, pcount):
    """打印进度条
    @param percent: 当前进度数
    @param pcount: 总共所需的进度
    """
    pcount = float(pcount)
    hashes = '#' * int(percent / pcount * 100)
    spaces = ' ' * (100 - len(hashes))
    sys.stdout.write("\rPercent: [%s] %0.2f%%" % (hashes + spaces, percent / pcount * 100))
    sys.stdout.flush()
    sleep(1)


def restartSvr():
    """重启服务器:切换到本目录下执行fab restartTestSvr(自动重启redis+memcache)
    """
    with settings(host_string=host, key_filename=key_filename, user=root, warn_only=True):
        run('supervisorctl stop ' + hostname)
        run('chown -R appuser:appuser /data')
    with settings(host_string=host, key_filename=key_filename, user=appuser, warn_only=True):
        print u"Please wait for memcache data to write the MysqlDB"
        with cd('/data/appsystems/appSvr01'):
            run('python synchrodata.py')  # 同步内存数据到mysqldb
        portList = [redis_port, memcahce_port]  # 测试服redis端口和memcache端口
        for ca in portList:
            try:
                run('kill -9' + ' ' + getPid(ca))
            except:
                pass
        for ca in range(5):  # 防止mem未启动
            run("/home/appuser/memcached-1.4.34/bin/memcached -p " + memcahce_port + " -d -m 2048 -u appuser -c 256 && echo 'start memcache success'", pty=False)
            if getPid(memcahce_port):
                break
            else:
                print "satrt memcached again:%s" % (4 - ca)
        for ca in range(5):  # 防止redis未启动
            run("/usr/local/bin/redis-server /data/appsystems/redis/conf/redis6370.conf && echo 'start redis success'", pty=False)  # pty=False 启动后台进程
            if getPid(redis_port):
                break
            else:
                print "satrt redis again:%s" % (4 - ca)

    with settings(host_string=host, key_filename=key_filename, user=root, warn_only=True):
        run('supervisorctl start ' + hostname)
        print "Restart restartSvr success"


if __name__ == '__main__':
    restartSvr()
