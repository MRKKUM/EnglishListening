from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired

# 登陆表单
# 继承flask_wtf 中的FlaskForm类
class LoginForm(FlaskForm):
    # 用户名 字符串类型 validators为验证器
    username = StringField(label=u'用户名',validators=[InputRequired('id不能为空')])
    # 密码    密码类型
    password = PasswordField(label=u'密码',validators=[InputRequired('密码不能为空')])
    # 提交  提交类型
    submit = SubmitField(label=u'登陆')