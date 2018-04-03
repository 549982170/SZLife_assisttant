# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月8日
@author: yizhiwu
工具类
'''
from collections import defaultdict
import collections
import datetime
from functools import wraps
import hashlib
from itertools import groupby
import json
import logging
from operator import itemgetter
import os
import platform
import re
import subprocess
import tempfile
from time import strftime, localtime, gmtime
import traceback
import unicodedata
import urllib
import urlparse
import uuid

from PIL import Image
from bs4 import BeautifulSoup
from docx import Document
from flask import url_for, request
from flask_login import current_user, login_required
import requests
from werkzeug._compat import text_type, PY2

import constants


configfiles = json.load(open(constants.configFilePath, 'r'))
logger = logging.getLogger()


def memotool(fun):
    """函数缓存装饰器"""
    cache = {}

    @wraps(fun)
    def wrap(*arg, **kwargs):
        key = str(arg) + str(kwargs)
        if key not in cache:
            cache[key] = fun(*arg, **kwargs)
        return cache[key]

    return wrap

def myrequest(url, tip="GET", payload={}, headers={}):
    """构造请求"""
    if tip == "GET":
        r = requests.get(url, data=payload, headers=headers)
    elif tip == "POST":
        r = requests.post(url, data=payload, headers=headers)
    elif tip == "PUT":
        r = requests.put(url, data=payload, headers=headers)
    elif tip == "DELETE":
        r = requests.delete(url, data=payload, headers=headers)
    else:
        return None
    return r.json()


def md5(ss):
    m = hashlib.md5()
    m.update(ss)
    return m.hexdigest()


def get_today_date():
    """
    获取今天的时间 int 20160907
    """
    return str(strftime("%Y%m%d", localtime()))


def get_dateobject(dtstr=None):
    """返回'1970-01-01 00:00:00'的时间对象"""
    if not dtstr:
        dtstr = '1970-01-01 00:00:00'
    return datetime.datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")


def get_dateStr():
    return datetime.datetime.now().__str__()[0:19]

def get_date_format(_format='%Y-%m-%d %H:%M:%S'):
    """ 返回时间字符串"""
    return str(datetime.datetime.now().strftime(_format))

def file_name(path):
    """获取文件名,如test.doc,返回test"""
    return os.path.splitext(path)[0]


def file_extension(path):
    """获取文件拓展名,如test.doc,返回.doc"""
    return os.path.splitext(path)[1]


def mysecure_filename(filename):
    """支持中文的获取文件名字函数"""
    _filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]')
    _windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1',
                             'LPT2', 'LPT3', 'PRN', 'NUL')
    if isinstance(filename, text_type):
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('utf-8', 'ignore')
        if not PY2:
            filename = filename.decode('ascii')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')

    filename = '_'.join(filename.split()).strip('._')
    if os.name == 'nt' and filename and \
                    filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename


def set_mysqldefaultbytable(tablename, values):
    """初始化数据表
    @param tablename: 表名
    @param values: 默认值
    @param player: player对象 
    """
    from app.db.dbentrust.dbpool import dbpool
    sql = "show columns from " + tablename
    updateMap = {}
    for ca in dbpool.querySql(sql, True):  # 初始化所有的列
        Field = str(ca['Field'])
        if Field == "UserId" and hasattr(current_user, "id"):
            updateMap[Field] = current_user.Data['Id']
        else:
            updateMap[Field] = values
    return updateMap

def is_chinese(contents):
    """判断是否仅为中文"""
    try:
        for ca in contents:
            if ca <= u"\u4e00" or ca >= u"\u9fa6":
                return False
        return True
    except:
        return False
    
def myconstructor(f, isdocx=False):
    """处理长文本生成器"""
    from app.db.dbadmin import get_syscfg_val
    for paragraph in f:
        if isdocx:
            paragraph = paragraph.text.encode('utf-8')
        if not paragraph:
            continue
        sceneheading = re.search('^\s*[0-9]+', paragraph)  # 匹配数字开头（场景）
        dialog = paragraph.replace("：", ":").replace(" ","").split(":")
        if sceneheading:
            num = sceneheading.group()
            Strtxt = "<p class='sceneheading' data-input='%s'>%s</p>" % (num, paragraph)
        elif dialog.__len__() > 1:  # 匹配冒号分隔（对话）  
            character = str(dialog[0])  # 人物
            dialogcontent = "".join(dialog[1:])  # 对话内容
            if is_chinese(character.decode("utf8")) and character.strip().decode("utf8").__len__().__str__() in get_syscfg_val(27).split("|"):  # 中文且长度在2~3个字符
                Strtxt = "<p class='character'>%s</p><p class='dialog'>%s</p>" % (character,dialogcontent)
            else:
                Strtxt = "<p class='action'>%s</p>" % paragraph
        else:
            Strtxt = "<p class='action'>%s</p>" % paragraph
        yield Strtxt

def readDocx(docName, pagenum=0):
    """获取docx的文档中的所有文字,不管格式,暂不支持doc格式每line行
    @param separated_rows: 文件
    @param pagenum: int 换页长度
    """
    TotalPage = 1  # 页数
    extension = os.path.splitext(docName)[1]  # 文件后缀名
    pagenum = int(pagenum)  # 换页长度
    line = 0
    if extension == ".txt":
        with open(docName) as f:
            flist = list(myconstructor(f))
            line = flist.__len__() -1  # 行数(多了一行---)
            docText = ''.join(flist)  # 生成器迭代对象优化性能
            docText = docText.split("-----------------------")[0]  # 去掉页码控制符,下标为1时是页码数
    elif extension == ".docx":
        paras = Document(docName)
        flist = list(myconstructor(paras.paragraphs, isdocx=True))
        line = flist.__len__()  # 行数
        docText = ''.join(flist)  # 生成器迭代对象优化性能区分传入对象
    else:
        docText = ""
    if pagenum != 0:
        num = line / pagenum # 页数
        TotalPage = num if num > 0 else 1
    return docText, TotalPage


def url_add_params(url, **params):
    """ 在url中加入新参数 
    url_add_params(http://www.google.com, token=123, site="bbs")
    return http://www.google.com?token=123&site=bbs
    """
    pr = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(pr.query))
    query.update(params)
    prlist = list(pr)
    prlist[4] = urllib.urlencode(query)
    return urlparse.ParseResult(*prlist).geturl()

def is_long(val):
    try:
        long(val)
        return True
    except:
        return False

def is_float(val):
    try:
        float(val)
        return True
    except:
        return False
    
def isalpha(Str):
    """判断是否为字母"""
    return Str.isalpha()

def isdigit(num):
    """判断是否为数字"""
    return num.isdigit()



def expect_float(num, remainder, default=None):
    """
    转换为 float 类型
    :param num:
    :param remainder:
    :param default:
    :return:
    """
    if not is_float(num):
        return default

    return round(float(num), remainder)


def startswith(Str, startTuple):
    """是否为startTuple字母开头
    @param Str: 源字符
    @param startTuple: 包含字符的数组（"x","y"）
    """
    return Str.startswith(startTuple)

def endswith(Str, endTuple):
    """是否为startTuple字母开头
    @param Str: 源字符
    @param endTuple: 包含字符的数组（"x","y"）
    """
    return Str.endswith(endTuple)

def myroute(f, url, g=login_required, needlogin=True, **kwargs):
    """必须登录的装饰器
    @parma f:蓝图的mod
    @parma url:路由url
    @parma g:login_required装饰器
    @param needlogin: True时为需要登录(默认) 
    """
    if needlogin:
        return lambda x: f.route(url, **kwargs)(g(x))
    else:
        return lambda x: f.route(url, **kwargs)(x)


def composed(*decs):
    """多个装饰器合并
    example:
    @composed(dec1, dec2)
    def some(f):
        pass
    """

    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f

    return deco


def endWith(*endstring):
    ends = endstring

    def run(s):
        f = map(s.endswith, ends)
        if True in f: return s

    return run


def processunicode(value):  # 定义一个处理unicode类型字符串的函数
    """中文转码"""
    v1 = ''
    for a in value:
        if type(a) == 'unicode':
            v1 = v1 + str(a.encoe('gb18030'))
    else:
        v1 = v1 + str(a)
    return v1


def getCoding(strInput):
    '''
         获取编码格式
    '''
    if isinstance(strInput, unicode):
        return "unicode"
    try:
        strInput.decode("utf8")
        return 'utf8'
    except:
        pass
    try:
        strInput.decode("gbk")
        return 'gbk'
    except:
        pass


def tranToUTF8(strInput):
    '''
    转化为utf8格式
    '''
    strCodingFmt = getCoding(strInput)
    if strCodingFmt == "utf8":
        return strInput
    elif strCodingFmt == "unicode":
        return strInput.encode("utf8")
    elif strCodingFmt == "gbk":
        return strInput.decode("gbk").encode("utf8")


def tranToGBK(strInput):
    '''
    转化为gbk格式
    '''
    strCodingFmt = getCoding(strInput)
    if strCodingFmt == "gbk":
        return strInput
    elif strCodingFmt == "unicode":
        return strInput.encode("gbk")
    elif strCodingFmt == "utf8":
        return strInput.decode("utf8").encode("gbk")


def smartToChangeCode(strInput):
    """根据平台转换编码,linux转utf8,windows转为gbk,适用于os.walk函数"""
    if 'Windows' in platform.system():
        return tranToGBK(strInput)
    else:
        return tranToUTF8(strInput)


def getplatform():
    """获取运行环境平台"""
    return platform.system()


def save_db_from(db_name, data):
    """保存数据到数据库
    data 是一个字典
    """
    updateMap = set_mysqldefaultbytable(db_name, 0)  # 初始化数据表默认值, 默认为0,初始化用户Id
    for k, v in data.items():
        updateMap[k] = v
    return updateMap


def parsed_dialogue(dlg, scene, shot_guid):
    """解析并保存对话数据
    """
    from app.db import memmode
    # 1-对话；2-独白
    type = 1 if dlg == 'dh' else 2
    db_dialogue = {}
    dialogue_num = 0
    for dialogue in scene.get(dlg, ''):  # 对话
        db_dialogue['Id'] = long(dialogue.get('id', 0))
        db_dialogue['Type'] = type  # 1-对话；2-独白
        db_dialogue['Contents'] = dialogue.get('content', '')  # 内容（选中的内容）
        db_dialogue['ShotGuid'] = shot_guid  # 镜头id
        # dialogue_num += len(db_dialogue['Contents'])  # 字数

        st_dialogueObj = memmode.st_dialogue.getObj(db_dialogue['Id'])
        if st_dialogueObj:
            st_dialogueObj.update_multi(db_dialogue)
        else:
            updateMap = save_db_from('st_dialogue', db_dialogue)
            memmode.st_dialogue.new(updateMap, True)

    # return dialogue_num


def get_effectTable(scene_id, _id=[], all=False):
    """ 特效
    scene_id： 场次 id
    """
    from app.db import memmode, dbadmin
    td = {}  # table body
    th = []  # table header
    effectpklist = memmode.st_effects.getAllPkByFk(scene_id)  # 获取所有的特效主键
    effectsObjList = memmode.st_effects.getObjList(effectpklist)  # 获取场次下所有特效Obj

    for cb in effectsObjList:
        etype = cb.get("data")['EffectsTypeId']
        eid = int(cb.get('data')['Id'])
        if all is False and eid not in _id:
            continue

        if etype == 2:  # 角色
            Name = cb.get("data")['Name']
            th.append(Name)
            td.setdefault(Name, set()).add(Name)  # 去重
        else:
            key = dbadmin.st_effectstype.get(etype).get('EName', '')  # EffectsType
            value = cb.get('data').get('Name', '')
            td.setdefault(key, set()).add(value)  # 去重
            th.append(key)

    td = {k: list(td.get(k)) for k, v in td.items()}  # 去重
    return td, th


def changeSqltupleByList(pklist):
    """
    @param pklist: 主键列表[5L,6L]
    @return: (5,6) 如果传入列表为一个元素[5L],则返回(5)去掉元组一个数据时后面的逗号
    """
    if pklist.__len__() > 1:
        return str(tuple(map(int, pklist)))
    else:
        return str(tuple(map(int, pklist))).replace(",", "")


def changeSqlStrByList(pklist):
    """
    @param pklist: 主键列表[5L,6L]
    @return: 5,6 如果传入列表为一个元素[5L],则返回5
    """
    return ",".join(map(str, pklist))


def get_shotTable(cid):
    from app.db import memmode, dbadmin
    shotPklist = memmode.st_shot.getAllPkByFk(cid)
    shotObjList = memmode.st_shot.getObjList(shotPklist)
    cnt_list = []
    id_list = []
    for shot in shotObjList:
        content = shot.get('data')['ShotContent']
        shotid = shot.get('data')['Guid']
        cnt_list.append(content)
        id_list.append(shotid)
    return cnt_list, id_list


def get_dialogueTable(shotid, type):
    from app.db import memmode, dbadmin
    r = []
    for id in shotid:
        dialoguePklist = memmode.st_dialogue.getAllPkByFk(id)
        dialogueObjList = memmode.st_dialogue.getObjList(dialoguePklist)
        for shot in dialogueObjList:
            if shot.get('data')['Type'] != type:
                continue
            content = shot.get('data')['Contents']
            r.append(content)
    return r


def tree():
    return defaultdict(tree)


def forTipsMsgUrl(msg):
    """
    @param msg: 提示的内容模版url
    """
    return url_add_params(url_for("index.tips"), msg=msg)


def sortedDictList(dict_list, dict_key, rev=False):
    """列表字典按字典里面的某个key来排序
    @param dict_list: list字典列表
    @param dict_key: str字典里面的某个key
    @param rev:bool 是否倒序,Flase为升序,True为降序
    """
    return sorted(dict_list, key=itemgetter(dict_key), reverse=rev)


def minDictList(dict_list, dict_key):
    """列表字典dict_key字段最小的字典
    @param dict_list: list字典列表
    @param dict_key: str字典里面的某个key
    """
    return min(dict_list, key=itemgetter(dict_key))


def maxDictList(dict_list, dict_key):
    """列表字典dict_key字段最大的字典
    @param dict_list: list字典列表
    @param dict_key: str字典里面的某个key
    """
    return max(dict_list, key=itemgetter(dict_key))


def dictListGroupby(dict_list, dict_key, rev=False):
    """按dict_key返回列表字典有序的分组字典,每组的key为dict_key
    @param dict_list: list字典列表
    @param dict_key: 分组的key
    @param rev:bool 是否倒序,Flase为升序,True为降序
    @return: 次数,列表字典
    """
    redata = collections.OrderedDict()
    dict_list.sort(key=itemgetter(dict_key), reverse=rev)
    for key, items in groupby(dict_list, key=itemgetter(dict_key)):
        redata[key] = []
        for i in items:
            redata[key].append(i)
    return redata


def dictListGroupby2(dict_list, dict_key, rev=False):
    """按dict_key返回列表字典有序的分组字典,每组的key为dict_key
    @param dict_list: list字典列表
    @param dict_key: 分组的key
    @param rev:bool 是否倒序,Flase为升序,True为降序
    """
    from app.db import memmode
    redata = collections.OrderedDict()
    dict_list.sort(key=itemgetter(dict_key), reverse=rev)
    for key, items in groupby(dict_list, key=itemgetter(dict_key)):
        redata[key] = []
        SceneInfo = {}
        SceneIdList = []
        for i in items:
            SceneId = i.get("SceneId")
            if SceneId not in SceneIdList:
                SceneIdList.append(SceneId)
        SceneInfoObjList = memmode.st_scene.getObjList(SceneIdList)
        Page = sum(float(ca.get('data')['Page']) for ca in SceneInfoObjList)
        SceneInfo['Page'] = Page  # 页数
        SceneInfo['SceneNum'] = len(SceneIdList)  # 场数        
        redata[key].append(SceneInfo)
    return redata


def unicodeclean(ustr):
    """清除和音字符
    @param ustr: unicode编码字符,如:u'pýtĥöñ is awesome\n'
    @return: 清除和音字符后的字符串'python is awesome\n'
    """
    return unicodedata.normalize('NFD', ustr).encode('ascii', 'ignore').decode('ascii')


def loggerJsonInfo(msg, Str="req:"):
    """打印json格式化的信息"""
    try:
        logger.info(Str + json.dumps(msg))
    except:
        logger.error(traceback.format_exc())


def str_limit(name, length=10):
    """按字节长度切割字符长度
    @param name: str 需要切割的字符串(第一个参数作为传入值)
    @param length: 需要切割的长度 
    """
    name = name.decode("utf-8")
    s = slice(length)  # 长度切片对象
    if len(name) <= length:
        redata = name
    else:
        redata = name[s] + "..."
    return redata


def getObjListByFk(memObj, fk):
    """根据外键获取主键Obj列表"""
    pklist = memObj.getAllPkByFk(fk)
    memObjList = memObj.getObjList(pklist)
    return memObjList


def delectdatabyFk(memmodeObj, fk, isSyncNow=False):  # 删除缓存对象
    Pklist = memmodeObj.getAllPkByFk(fk)
    for ca in Pklist:
        memmodeObj.deleteMode(ca, isSyncNow)


def getLoginPageUrl():
    """获取登录页url"""
    from app.db.dbadmin import get_syscfg_val
    IndexURL = get_syscfg_val(15) + get_syscfg_val(10)  # SOOVII登录页URL
    redirectURL = url_add_params(IndexURL, ReturnUrl=configfiles['loginUrl'])  # 追加跳转到本服务器参数url
    return redirectURL


def changedoc2docxbywin32(fpath, tpath):
    """把doc文件转换为docx因为用到win32com,所以仅支持windows系统
    @param fpath: 文件绝对路径,不能包含中文
    @param tpath: 文件绝对保存路径,不能包含中文"""
    try:
        from win32com import client
        import pythoncom
        pythoncom.CoInitialize()
        word = client.DispatchEx('Word.Application')  # 独立进程
        word.Visible = 0  # 不显示
        word.DisplayAlerts = 0  # 不警告
        doc = word.Documents.Open(fpath)
        doc.SaveAs(tpath, 12)  # 参数16是保存为doc,转化成docx是12
        doc.Close()
        word.Quit()
        return True
    except:
        logger.error(traceback.format_exc())
        if doc:
            doc.Close()
        word.Quit()
        return False


def chang2txtbyantiword(fpath, tpath):
    """通过antiword读取doc,需要安装antiword,目前仅用于linux(详情见:http://www.winfield.demon.nl)
    wget http://www.winfield.demon.nl/linux/antiword-0.37.tar.gz
    tar -xvf antiword-0.37.tar.gz
    cd antiword-0.37
    make && make install 
    @param fp: 相对文件路径"""
    try:
        com = "antiword -m UTF-8.txt -w 0 -f " + fpath + " > " + tpath
        out_temp = tempfile.SpooledTemporaryFile(bufsize=10 * 1000)
        fileno = out_temp.fileno()
        obj = subprocess.Popen(com, shell=True, stdout=fileno, stderr=fileno)
        output = obj.wait()
        out_temp.seek(0)
        #         lines = out_temp.readlines()
        if output == 0:  # 执行成功
            return True
        return False
    except:
        logger.error(traceback.format_exc())
        return False
    finally:
        if out_temp:
            out_temp.close()


def getCodePwd():
    """获取代码根目录绝对路径"""
    return os.getcwd()


def compareTimeByStr(timeSrt1, timeSrt2, formatType='%Y-%m-%d %H:%M:%S'):
    """比较字符串时间大小
    @param timeSrt1: 时间字符串1（Str）
    @param timeSrt2: 时间字符串2（Str）
    @return: timeSrt1>timeSrt2的boolean值（True/Flase）"""
    try:
        d1 = datetime.datetime.strptime(str(timeSrt1), formatType)  # 字符串转日期
        d2 = datetime.datetime.strptime(str(timeSrt2), formatType)  # 字符串转日期
        return d1 > d2
    except:
        logger.error(traceback.format_exc())
        return False

def formatNum(num, digit=0):
    """字符串格式化位数"""
    try:
        num = int(num)
        return ("%0" + str(digit) + "d") % num
    except:
        return num
    
def changBit2Int(num_2):
    """二进制转十进制"""
    try:
        return int("0b" + str(num_2), 2)  # 转为10进制
    except:
        return 0
    
def changInt2Bit(num, tip=16):
    """十进制转二进制,八进制,16进制"""
    try:
        num = int(num)
        if tip==2:
            return bin(num)  # 十进制转二进制
        if tip==8:
            return oct(num)  # 十进制转八进制
        if tip==16:          
            return hex(num)  # 十进制转十六进制
        else:
            return num  # 十进制转十进制
    except:
        return 0
    
def getsqlsbylist(sqlList):
    """生成列表长度的sql的s个数"""
    try:
        if isinstance(sqlList, list):
            return ("%s," * len(sqlList)).rstrip(",")
        return ""
    except:
        return ""



def checklen(pwd, start=0, limit=6):
    """
    校验字符串长度
    :param pwd:
    :param limit:
    :return:
    """
    return len(pwd) >= int(start) and len(pwd) <= int(limit)


def checkSymbol(pwd):
    """
    校验字符串是否包含数字或字母
    :param pwd:
    :return:
    """
    pattern = re.compile('([^a-z0-9A-Z])+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False

def checkOnlyNum(num):
    """
    校验字符串是否只包含数字
    :param num:
    :return:
    """
    pattern = re.compile('^[0-9]*$')
    match = pattern.match(num)
    if match:
        return True
    else:
        return False

def valid_phone(phone_num):
    """
    校验手机号码
    :param phone_num:
    :return:
    """
    # 判断长度是否合法
    len_ok = checklen(phone_num, start=11, limit=11)

    # 判断是否只包含数字
    num_ok = checkOnlyNum(phone_num)

    return num_ok and len_ok

def checkEmail(email):
    """
    校验字符串是否只包含数字或字母
    :param num:
    :return:
    """
    pattern = re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    match = pattern.match(email)
    if match:
        return True
    else:
        return False


def checkOnlySymbol(pwd):
    """
    校验字符串是否只包含数字或字母
    :param num:
    :return:
    """
    pattern = re.compile('^[0-9a-zA-Z]+$')
    match = pattern.match(pwd)
    if match:
        return True
    else:
        return False

def filegenerate(filename):
    """大文件生成二进制迭代器
    @param filename: 文件路径"""
    with open(filename, 'rb') as r:
        for line in r:
            yield line

def getUploadFilePath(path=""):
    """获取上传的路径地址"""
    from app.share.constants import UPLOAD_FOLDER
    f_path = os.path.join(UPLOAD_FOLDER, path)  # 文件存放相对路径
    if not os.path.exists(f_path):
        os.makedirs(f_path)
    return f_path

def clipimage(size):
    width = int(size[0])
    height = int(size[1])
    box = ()
    if (width > height):
        dx = width - height
        box = (dx / 2, 0, height + dx / 2,  height)
    else:
        dx = height - width
        box = (0, dx / 2, width, width + dx / 2)
    return box

def compressPic(fp,width=500, height=500, addname="_thumb"):
    """裁剪为正方形"""
    im = Image.open(fp)
    box = clipimage(im.size)
    img = im.crop(box)
    size = (width, height)
    img.thumbnail(size, Image.ANTIALIAS)
    extension = os.path.splitext(fp)[1]
    filename = fp.replace(extension,addname+extension).replace("\\","/")
    img.convert('RGB').save(filename, "JPEG")
    return filename

def getUploadActorImgPath(extension, pname):
    from app.share.constants import ACTORFPATH
    dateStr = get_today_date()  # 日期
    uuidfilename = str(uuid.uuid1()) + extension  # 随机文件
    folder = os.path.join(ACTORFPATH, dateStr, pname)  # 上传文件保存路径
    filepath = os.path.join(getUploadFilePath(folder), uuidfilename).replace("\\","/")
    return filepath

def getClentRealIP():
    """获取客户端真实IP"""
    try:
        ip = request.remote_addr
        _ip = request.headers["X-Real-IP"]  # 配合nginx获取IP
        if _ip is not None:
            ip = _ip
            msg = "The X-Real-IP is: %s"
    except:
        msg = "The remote_addr is: %s"
    finally:
        logger.info(msg % ip)
        return ip
        
def CompressPic(filename, addname="_thumb"):
    """转换为压缩图"""
    tpath = filename
    if addname not in filename:
        extension = os.path.splitext(filename)[1]  # 文件拓展名
        tpath = filename.replace(extension, addname+extension, 1)        
    return tpath

def countage(dateStr):
    """计算年龄工具
    @param dateStr(string): 2016-07-5 10:15:07
    @return: 年龄age"""
    dateObj = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
    d = dateObj.day
    m = dateObj.month
    y = dateObj.year
    a = gmtime()
    # difference in day
    dd = a[2] - d
    # difference in month
    dm = a[1] - m
    # difference in year
    dy = a[0] - y
    # checks if difference in day is negative
    if dd < 0:
        dd = dd + 30
        dm = dm - 1
        # checks if difference in month is negative when difference in day is also negative
        if dm < 0:
            dm = dm + 12
            dy = dy - 1
    # checks if difference in month is negative when difference in day is positive
    if dm < 0:
        dm = dm + 12
        dy = dy - 1
    return dy

def getStrOnly(Str):
    """仅仅获取字符(过滤特殊符号和html标签等)"""
    pattern = re.compile(r'\S')
    maybehtml = "".join(pattern.findall(Str))
    soup = BeautifulSoup(maybehtml, 'lxml')
    soup.prettify()  # 标准化
    return str(soup.get_text())


