from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField,SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,EqualTo,ValidationError
from .models import User 
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password  = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('SignUp')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken please choose another username')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError('Email is already taken please choose another email.')

class LoginForm(FlaskForm):
    #username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password  = PasswordField('Password',validators=[DataRequired()])
    #confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    rememberme = BooleanField('Remember Me',)
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    # password  = PasswordField('Password',validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg', '_png_'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken please choose another username')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user: 
                raise ValidationError('Email is already taken please choose another email.')
            



class PostForm(FlaskForm):
    title = StringField('Title',validators = [DataRequired()])
    content = TextAreaField('Content',validators = [DataRequired()])
    submit = SubmitField('Post')