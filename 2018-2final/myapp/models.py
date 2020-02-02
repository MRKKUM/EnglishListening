from flask_mongoengine import MongoEngine
from jieba.analyse.analyzer import ChineseAnalyzer
from flask import Flask


# 实例化一个Flask对象
app = Flask(__name__)
# 进行数据库的相关配置
app.config['MONGODB_SETTINGS'] = {
    'db': '201802final',
    'host': '127.0.0.1',
    'port': 27017
}
# 实例化一个数据库对象
db = MongoEngine(app)

# Todo类 对应数据库当中的 data_link 集合
class Todo(db.Document):
    meta = {
        'collection': 'data_link',
        'ordering': ['-create_at'],
        'strict': False,
    }
    __searchable__ = ['file_name']
    __analyzer__ = ChineseAnalyzer()

    file_name = db.ListField()
    src = db.ListField()

# 分页操作 data_link数据很多
def view_todos(page):
    return Todo.objects.paginate(page=page, per_page=10)

# User类 对应数据库中的 user_info 类
class User(db.Document):
    meta = {
        'collection': 'user_info',
        'ordering': ['-create_at'],
        'strict': False,
    }

    user_id = db.StringField()
    user_pwd = db.StringField()



