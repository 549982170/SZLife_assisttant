# coding:utf-8
#!/user/bin/python
'''
Created on 2017年7月12日
@author: yizhiwu
工具箱
'''
import datetime
import platform

def getCompareDateByStr(timeSrt1, timeSrt2, formatType='%Y%m%d'):
    """比较获取字符串时间间隔
    @param timeSrt1: 时间字符串1（Str）
    @param timeSrt2: 时间字符串2（Str）
    @return: timeSrt1>timeSrt2的boolean值（True/Flase）"""
    try:
        d1 = datetime.datetime.strptime(str(timeSrt1), formatType)  # 字符串转日期
        d2 = datetime.datetime.strptime(str(timeSrt2), formatType)  # 字符串转日期
        return (d1 - d2).days
    except:
        return 0
    
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
