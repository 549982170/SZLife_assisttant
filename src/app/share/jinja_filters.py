# coding:utf-8
#!/user/bin/python
'''
Created on 2017年3月27日
@author: yizhiwu
拓展的jinja2模版过滤器函数,如需要新增直接增加函数即可，使用时
'''
import datetime
import os


def length_limit(name, length=10):
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

def date_limit(Str, length=10):
    """截取时间对象日期"""
    if Str:
        return str(Str)[0:length]
    else:
        return ""
    
def isNoneDate(date):
    """判断时间对象是否存在"""
    if not date or str(date) == "1900-01-01 00:00:00":  # 不存在日期
        return True
    return False

def mydefault(data, Str):
    """不存在时设置默认字符"""
    if not data or data == "0" or data=="":
        return Str
    return data

def mysetjoin(dataList, Str, NoneStr=""):
    """去重列表表字符串"""
    if isinstance(dataList, list) or isinstance(dataList, set) and dataList:
        if len(dataList) >= 1 and list(dataList)[0] is None:
            return NoneStr
        else:
            return (Str).join(dataList)
    return NoneStr

def mysortlistjoin(dataDict, mylist, Str, NoneStr=""):
    """列表字典"""
    if not dataDict:
        return NoneStr
    datalist = []
    for ca in mylist:
        if dataDict.get(ca) and ca not in datalist:
            datalist.append(ca)
    return Str.join(datalist)


def sequene_sortlistjoin(actor_list, title_list, separator, defualt=""):
    """顺场景表列表字典排序"""
    if not actor_list:
        return defualt
    ret = []
    for ca in title_list:
        name = ca.get('Name', '')
        if name in actor_list and name not in ret:
            ret.append(name)
    return separator.join(ret)


def formatDigit(num, digit=0):
    """字符串格式化位数"""
    try:
        num = int(num)
        return ("%0" + str(digit) + "d") % num
    except:
        return ""
    
def formatRaund(num, digit=0):
    """字符串格式化位数"""
    try:
        if num == "0.0" or float(num) <= 0 or isinstance(num, str):
            return ""
        num = float(num)
        return ("%." + str(digit) + "f") % num
    except:
        return ""

def myimgPath(Str):
    if "xxx" in Str:
        return True
    return False

def formate_date(mydate):
    """把日期:2017-04-24 00:00:00字符串格式化为2017年4月11号 星期二"""
    if not formate_date or formate_date=="":
        return ""
    weekdaydict = {0:u"一", 1:u"二", 2:u"三", 3:u"四", 4:u"五", 5:u"六", 6:u"日"}
    t_str = str(mydate)[0:10]
    d = datetime.datetime.strptime(t_str, '%Y-%m-%d')  # 字符串转日期
    datastr = ""
    datastr += str(d.year) + "年"
    datastr += str(d.month) + "月"
    datastr += str(d.day) + "日"
    datastr += " 星期" + str(weekdaydict.get(d.weekday()))
    return datastr
    


def total_actors_num(actors):
    """
    演员列表总数
    :param actors: 演员列表
    :return:
    """
    totalnum = 0
    for actor in actors:
        totalnum += actor.get('Num', 0)
    return totalnum


def getStr(arr):
    """
    顺场景表为表格换行
    :param arr: 数组，数组元素为字符串
    :return:
    """
    result = ''
    if arr:
        for a in arr:
            result += a + "<br>"
    return result


def  getupdatetime(updatetime, createtime):
    if updatetime and createtime!=updatetime:
        return updatetime
    return ""



def mycheckPermission(u, code):
    """ 校验权限 """
    from app.db.dbadmin import ac_role
    from flask_login import current_user

    role = dict(ac_role)
    r = role.get(code)
    status = current_user.checkPermission(r.get('Code', 0))
    return status

def CompressPic(filename, addname="_thumb"):
    """转换为压缩图"""
    tpath = filename
    if addname not in filename:
        extension = os.path.splitext(filename)[1]  # 文件拓展名
        tpath = filename.replace(extension, addname+extension, 1)        
    return tpath
