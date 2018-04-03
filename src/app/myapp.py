# coding:utf-8
#!/user/bin/python
'''
Created on 2017年6月23日
@author: yizhiwu
路由文件
'''
from views import index


def register_blue(app):
    # 业务模块
    app.register_blueprint(index.mod)

