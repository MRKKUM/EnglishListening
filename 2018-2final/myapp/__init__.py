from flask import Flask
import flask_wtf
from .views import main
import os

#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
# 添加配置信息
# session加密
app.config['SECRET_KEY']=os.urandom(32)
# csrf 跨站请求伪造 保护
flask_wtf.CSRFProtect(app)
# 注册蓝图
app.register_blueprint(main)
app.register_blueprint(main,url_prefix='/index')


