from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import InputRequired, Length, AnyOf, Email
from Flaskblog import User
from appInit import app, db 
import database
from flask_bcrypt import Bcrypt

Bootstrap(app)
bcrypt = Bcrypt(app)

#database.drop()
database.createdb()

class loginForm(FlaskForm):
    email = StringField('Email Address', validators=[Email('Email is REQUIRED!'),
                                                     Length(min=6, max=35)])

    password = PasswordField('Password', validators=[InputRequired('Password is REQUIRED!'),
                                                     Length(min=8, message='Must be one Uppercase letter and one number'
                                                                           ' and symbol ')])


class RegisterForm(FlaskForm):
    username = StringField('Name', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=5, max=20, message='Must be filled')])

    password = PasswordField('Password', validators=[InputRequired('Password is REQUIRED!'),
                                                     Length(min=8, message='Must be one Uppercase letter and one number'
                                                                           ' and symbol ')])

    email = StringField('Email Address', validators=[Email('Email is REQUIRED!'),
                                                     Length(min=6, max=35)])
    recaptcha = RecaptchaField()

@app.route('/')
def base():
  return render_template('base.html')


@app.route('/login', methods=['GET', 'POST']) 
def login():
    login = loginForm()

    if login.validate_on_submit():
      user = User.query.filter_by(email = format(login.email.data)).first()
      if user == None:
        flash(f'Email or password wrong', category = 'success')
      else:
        if user.email == format(login.email.data) and bcrypt.check_password_hash(bcrypt.generate_password_hash(format(login.password.data), 10), user.password) == True:
          flash(f'Welcome {user.username}', category = 'success')
        else:
          flash(f'Email or password wrong', category = 'success')
    return render_template('login.html', login=login)


@app.route('/register', methods=['GET', 'POST']) 
def register():
    register = RegisterForm()

    if register.validate_on_submit():
      user = User()
      if User.query.filter_by(email = format(register.email.data)).first() == None:
        user.username = format(register.username.data)
        user.email = format(register.email.data)
        user.password = bcrypt.generate_password_hash(format(register.password.data), 10)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {register.username.data}!', category = 'success')
        return redirect(url_for('login'))
      else:
        flash(f'This user already exist', category = 'success')
    return render_template('register.html', register=register)



@app.route('/posts')
def posts():
  return render_template('posts.html')


if __name__ == '__main__':
    app.run(debug=True)
