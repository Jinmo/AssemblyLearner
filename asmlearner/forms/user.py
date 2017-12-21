from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from asmlearner.db.models.user import User


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        user_ = User.login(self.name.data, self.password.data)
        if user_:
            self.user = user_
            return True
        else:
            return False


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if not User.exists(self.name.data):
            User.create(name=self.name.data, password=self.password.data)
            return True
        return False
