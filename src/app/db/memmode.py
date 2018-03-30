# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月10日
@author: yizhiwu
内存对象集,可直接添加内存对象
'''
from dbentrust.madminanager import MAdminManager
from dbentrust.mmode import MAdmin

# ---------------添加的内存库表----------------
ac_users = MAdmin('ac_users', 'Id', fk='AccountId')  # 用户表
ac_users.insert()
MAdminManager().registe(ac_users)
