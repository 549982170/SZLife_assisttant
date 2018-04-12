# coding:utf-8
#!/user/bin/python
'''
Created on 2017年6月23日
@author: yizhiwu
路由文件
'''
from views import admin_user
from views import index
from views import user


def register_blue(app):
    # 业务模块
    app.register_blueprint(index.mod)
    app.register_blueprint(user.mod, url_prefix='/user')

    # admin
    app.register_blueprint(admin_user.mod, url_prefix='/admin')

