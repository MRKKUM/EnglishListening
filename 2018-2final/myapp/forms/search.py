from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import InputRequired

# 搜索表单
# 继承flask_wtf 插件中的FlaskForm类
class SearchForm(FlaskForm):
    # 关键字 validators为验证器
    key_word = StringField(label=u'用户名',validators=[InputRequired('不能为空')])
    # 提交
    submit = SubmitField(label=u'Search')