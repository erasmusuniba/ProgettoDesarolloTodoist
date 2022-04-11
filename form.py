from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError,TimeField, DateField,SelectField
from flask_wtf.file import FileField, FileRequired

from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import UserModel, Category, Todo


#Creazione del modulo per accedere 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                       Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.')

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered.')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', coerce=int , validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d' , validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M' , validators=[DataRequired()])
    submit = SubmitField('Add task')




class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description' , validators=[DataRequired()])
    image =  FileField(validators=[FileRequired()])
    submit = SubmitField('Add task')