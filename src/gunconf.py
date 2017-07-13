# coding:utf-8
#!/user/bin/python
'''
Created on 2017年4月7日
@author: yizhiwu
gunicorn 配置文件
'''
import os
import json

import multiprocessing
import gevent.monkey

gevent.monkey.patch_all()

# 配置文件
configFilePath = os.path.join('config', 'config.json')
configfiles = json.load(open(configFilePath, 'r'))

# gunicorn配置
bind = configfiles['host'] + ":" + str(configfiles['port'])   # 绑定的ip已经端口号
timeout = 30                                             # 超时
worker_class = 'gevent'                                  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
loglevel = 'info'                                        # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置
accesslog = "/dev/null"                                  # 访问日志文件的路径
errorlog = "./log/gunicorn_errorlog.log"                 # 错误日志文件的路径
pidfile = "./log/gunicorn.pid"


#启动的进程数
# workers = multiprocessing.cpu_count() * 2 + 1            # 进程数(子进程共享了父进程的文件句柄,多进程共用一个 fd 的情况下使用 logging 模块写少量日志是进程安全的) 
workers = 4
threads = 2                                              # 指定每个进程开启的线程数
backlog = 512                                            # 监听队列
