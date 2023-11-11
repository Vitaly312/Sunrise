from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app import db
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Логин: ', validators=[DataRequired()],
                          render_kw={'class': 'form-control'})
    password = PasswordField('Пароль: ', validators=[DataRequired()],
                            render_kw={'class': 'form-control'})

class BaseUserSignup(FlaskForm):
    email = StringField("Адрес электроной почты", validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control', 'placeholder': "name@example.com"})
    password = PasswordField('Пароль: ', render_kw={'class': 'form-control'},
                             validators=[DataRequired(), Length(min=8, max=30)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})

    def validate_email(form, field):
        if db.session.query(User).filter(User.email == field.data).first():
            raise ValidationError('Пользователь с таким E-mail уже зарегестрирован')

    def validate_password2(form, field):
        if form.password.data != field.data:
            raise ValidationError("Пароли не совпадают")

class SignUpForm(BaseUserSignup):
    name = StringField("Ваше имя:", validators=[DataRequired()], render_kw={'class': 'form-control'})
    gender = RadioField('Пол', choices=[(0, 'Мужской'), (1, "Женский")], default=0, render_kw={'class': 'form-control'})

class CreateTaskForm(FlaskForm):
    title = StringField("Название задачи", validators=[DataRequired(), Length(max=150)], render_kw={'class': 'form-control'})
    description = TextAreaField('Описание задачи', validators=[Length(max=5000)], render_kw={'class': 'form-control', 'rows': '5'})

