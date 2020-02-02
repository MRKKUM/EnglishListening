from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,EqualTo

# 注册表单
# 继承flask_wtf插件中的FlaskForm类
class SignForm(FlaskForm):
    # 用户名 validators为验证器
    username = StringField(label=u'用户名',validators=[InputRequired('id不能为空')])
    # 设置密码
    password = PasswordField(label=u'设置密码',validators=[InputRequired('密码不能为空')])
    # 重复密码 需要和上一次输入的密码一致
    repeat_password = PasswordField(label=u'重复密码', validators=[InputRequired('密码不能为空'),EqualTo('password')])
    # 提交按钮
    submit = SubmitField(label=u'注册')