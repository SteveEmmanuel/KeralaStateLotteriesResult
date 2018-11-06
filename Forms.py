from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from wtforms_alchemy import ModelForm
from flask_wtf import Form
import json


class JSONField(TextAreaField):
    def _value(self):
        return json.dumps(self.data) if self.data else ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = json.loads(valuelist[0])
            except ValueError:
                raise ValueError('This field contains invalid JSON')
        else:
            self.data = None

    def pre_validate(self, form):
        super().pre_validate(form)
        if self.data:
            try:
                json.dumps(self.data)
            except TypeError:
                raise ValueError('This field contains invalid JSON')

class LotteryForm(ModelForm):
    class Meta:
        only = ['name', 'date', 'series']
    details = JSONField()

class LoginForm(Form):
    """Form class for user login."""
    user_id = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])