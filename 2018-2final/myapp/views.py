from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask import render_template
from flask import request
from functools import wraps
from .models import User,Todo
import myapp.models as db
from .forms.login import LoginForm
from .forms.sign import SignForm
from .forms.search import SearchForm
from .search import do_search

# 创建蓝图
main=Blueprint('main',__name__)

# 权限控制 相当于jfinal中的拦截器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查session是否是空的,每一个线程都对应一个session
        if session.get('user_id') == '' or session.get('user_id') == None:
            # 消息闪现 可以作为提示信息等 基于session实现
            flash('请登陆!')
            # 跳转页面 重定向 注意 url_for 的参数为方法名称
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function

# 主页映射 注解 url_map 将来注册蓝图之时,添加到url_map映射中
@main.route('/')
def index():
    # 实例化搜索表单
    form_search = SearchForm()
    # 渲染页面 传递表单参数
    return render_template('index.html',form_search=form_search)

# 登陆映射
@main.route('/login',methods=["GET","POST"])
def login():
    # 判断请求的方式
    if request.method == 'GET':
        form_search = SearchForm()
        form = LoginForm()
        return render_template('login.html', form=form,form_search=form_search)
    else:
        form = LoginForm(request.form)
        # 对表单内容是否通过验证进行判断
        if form.validate():
            # 获取表单的数据
            data = form.data
            # 数据库查询
            admin = User.objects(user_id=data['username'], user_pwd=data['password']).first()
            # 对查询结果进行判断
            if not admin:
                flash('密码错误或用户不存在！')
                return redirect(url_for('main.login'))
            else:
                flash('Successfully logged in!')
                session['user_id'] = data['username']
                return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.login'))

# 注销映射
@main.route('/logout')
def logout():
    flash('已退出登陆！')
    # 从session中删除即可
    session.pop('user_id')
    return  redirect(url_for("main.index"))

# 注册映射
@main.route('/sign',methods=["GET","POST"])
def sign():
    # 判断请求方式
    if request.method == 'GET':
        form_search = SearchForm()
        form = SignForm()
        return render_template('sign.html', form=form,form_search=form_search)
    else:
        form = SignForm(request.form)
        print('注册表单验证:',form.validate_on_submit())
        # 判断表单是否通过验证
        if form.validate():
            data = form.data
            # 通过查询结果判断 是否已存在该用户
            admin = User.objects(user_id=data['username']).first()
            if not admin:
                flash('注册成功!')
                User(user_id=data['username'],user_pwd=data['password']).save()
                return redirect(url_for('main.index'))
            else:
                flash('用户已存在!')
                return redirect(url_for('main.sign'))
        else:
            flash('输入格式有误!')
            return redirect(url_for('main.sign'))

# 为方便查看数据所有用户
@main.route('/allUser')
def all_user():
    form_search = SearchForm()
    users = User.objects().all()
    return render_template('allUser.html', users=users,form_search=form_search)

# 听力入门页面 映射 以及拦截认证注解
@main.route('/entryLevel')
@admin_login_req
def entry_level():
    form_search = SearchForm()
    # 获取get请求传过来的页数,没有传参数，默认为1
    page = int(request.args.get('page', 1))
    # 调用数据库分页的方法进行查询
    paginate  = db.view_todos(page)
    # Pagination object的内容
    stus = paginate.items
    return render_template('entryLevel.html', files=stus, paginate=paginate,form_search=form_search)

# 听的界面
@main.route('/listenIt')
def listen_it():
    form_search = SearchForm()
    args = dict(request.args)
    data_id = args['id']
    print(data_id[0])
    # 判断是从搜索页面来的 还是通过听力入门界面来的
    if len(data_id[0]) == 24 :
        file = Todo.objects(id=data_id[0]).first()
    else:
        file = Todo.objects().skip(
            int(data_id[0])-1
        ).first()
    return render_template('listenIt.html', file=file,form_search=form_search)

# 搜索处理方法
@main.route('/search', methods = ['POST'])
def search():
    form = SearchForm(request.form)
    form_search = SearchForm()
    data = form.data
    key_word = data['key_word']
    # 进行检索
    results = do_search(key_word)
    return render_template('search_results.html',form_search=form_search,results=results,query=key_word)

# 404页面
@main.errorhandler(404)
def page_404(er):
    return render_template('404.html',er = er)
