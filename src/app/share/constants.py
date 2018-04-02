# coding:utf8
"""
定义系统常量
Created on 2017年2月8日
@author: yizhiwu
"""
import os
import collections
from logging import config

# ---------------Start-----------------------------------
configFilePath = os.path.join('config', 'config.json')                  # 配置文件路径
logFilePath = os.path.join('config', 'logger.conf')                     # 默认配置日志路径
defaultStaticFolder = os.path.join('app', 'website', 'static')          # 默认static文件路径
defaultTemplateFolder = os.path.join('app', 'website', 'templates')     # 默认templates文件路径
defaultMediaFolder = os.path.join('..', '..', 'media')                  # 默认media文件路径
adminstaticFolder = os.path.join('..', '..', '..', 'static', 'admin')         # admin蓝图static文件路径
admintemplateFolder = os.path.join('..', '..', '..', 'templates', 'admin')    # admin蓝图templates文件路径
adminMediaFolder = os.path.join('..', '..', '..', '..', 'media', 'admin')       # admin蓝图的media文件路径
mediaFolder = os.path.join('media')                                     # media文件路径
DEFAULT_ENCODING = 'utf-8'                                              # 默认编码
SECONDS = 60                                                            # memcache数据同步到mysql扫描时间间隔
UPLOAD_FOLDER = os.path.join('media', 'upload')                         # 上传的文件路径
IGNOREURL = ['/user/login', '/user/index.js.map']                       # 忽略跳转到登录的url,index.js.map为jquery获取min.map的url
CharacterEffectsType = 2                                                # 角色特效类型
CGEffectsType = 1                                                       # CG特效类型
EffectEtypeId = collections.OrderedDict([('cj', 3), ('js', 2), ('cg', 1), ('dj', 5), ('fx', 21), ('hz', 17), ('fz', 33), ('wx', 43), ('tj', 44), ('jiaotong', 37), ('dw', 45)])  # 特效类型
WkhtmltopdfPath = "D:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"               # windows系统PDF下载软件wkhtmltopdf软件路径
STATUS_EDIT = 1                                                        # 剧本状态编辑状态
STATUS_STANDARDIZATION = 1                                              # 剧本状态标准化状态
STATUS_SPLIT = 2                                                        # 剧本状态拆分状态
SOCP = "common"                                                         # 登录请求socp
GRANT_TYPE = "password"                                                 # 登录请求grant_type
GRANT_TYPE2 = "refresh_token"                                           # 刷新token请求grant_type
ALLOWED_EXTENPICSIONS = [".jpg", ".png", ".bmp", ".jpeg"]                # 上传图片的限制格式
ACTORFPATH = "actor"                                                    # 演员图片文件夹


# ---------------END-----------------------------------
config.fileConfig(logFilePath)  # 配置日志
