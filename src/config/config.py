# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月13日
@author: yizhiwu
falsk配置类
'''
import json
from app.share.constants import configFilePath

configfiles = json.load(open(configFilePath, 'r'))  # 配置文件

class Config(object):
    DEBUG = True if configfiles['debug'] == "True" else False
    SECRET_KEY = configfiles['secret_key']  # 键值跟企业中心一致
    REMEMBER_COOKIE_NAME = configfiles['REMEMBER_COOKIE_NAME']  # 键值 跟企业中心一致
    WTF_CSRF_TIME_LIMIT = configfiles['sessionMinutes']  # CSRF跨域验证有效时间,防止冲突,跟session时间一致
    WTF_CSRF_CHECK_DEFAULT = configfiles['secret_key']  # 键值跟企业中心一致
    MAX_CONTENT_LENGTH = 1024 * 1024 * int(configfiles['maxcontentlength'])  # 最大上传文件字节(M)

    