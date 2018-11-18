from wtforms import StringField, PasswordField, TextAreaField, SubmitField, Form
from wtforms_alchemy import ModelForm
import json
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm, RecaptchaField

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

class LoginForm(FlaskForm):
    """Form class for user login."""
    user_id = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FeedBackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(min=6, max=50)])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
    recaptcha = RecaptchaField('Captcha')

    '''def validate(self):
        valid = True
        if not Form.validate(self):
            valid = False
        if not self.email.data:
            self.email.errors.clear()
            self.email.errors.append("Email required")
            valid = False
        if not self.name.data:
            self.name.errors.clear()
            self.name.errors.append("Name required")
            valid = False
        if not self.comment.data:
            self.comment.errors.clear()
            self.comment.errors.append("Comment required")
            valid = False
        valid = False

        return valid'''
