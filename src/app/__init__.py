# coding:utf-8
#!/user/bin/python
'''
Created on 2017年3月2日
@author: yizhiwu
改变项目编码为utf-8,防止ascii编码字符串转换成"中间编码" unicode 时由于超出了其范围
也可以在/usr/lib/python2.7/site-packages/目录下添加一个sitecustomize.py文件
import sys
sys.setdefaultencoding('utf-8')
link https://my.oschina.net/yves175/blog/849704
'''
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)