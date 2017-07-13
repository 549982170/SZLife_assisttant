# coding:utf-8
#!/user/bin/python
'''
Created on 2017年6月1日
@author: yizhiwu
'''
# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月14日
@author: yizhiwu
用户类
'''
import datetime
import logging
import traceback

from flask_login import UserMixin

logger = logging.getLogger("adminlog")

class adminUser(UserMixin):
    
    
    def __init__(self, uid):
        self.uid = uid
    
    @property
    def id(self):
        return self.uid
    
        
            
            

