import wtforms
from wtforms.validators import length

class LoginForm(wtforms.Form):
    username=wtforms.StringField(validators=[length(min=6,max=20)])

    password=wtforms.StringField(validators=[length(min=6,max=20)])
