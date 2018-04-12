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
tb_users = MAdmin('tb_users', 'id', fk='')  # 用户表
tb_users.insert()
MAdminManager().registe(tb_users)

tb_admin_users = MAdmin('tb_admin_users', 'id', fk='')  # 用户表
tb_admin_users.insert()
MAdminManager().registe(tb_admin_users)
