from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, AnyOf, Email, EqualTo, ValidationError, Regexp
from Flaskblog import User
from appInit import app, db
import database
import os
import secrets
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required 
from flask_wtf.file import FileField, FileAllowed
from PIL import Image


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
    remember = BooleanField('Remember Me')


class RegisterForm(FlaskForm):
    username = StringField('Name', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=5, max=20, message='Must be filled')])

    password = PasswordField('Password', validators=[InputRequired('Password is REQUIRED!'),
                                                     Length(min=8, message='Must be one Uppercase letter and one number'
                                                                           ' and symbol ')])

    email = StringField('Email Address', validators=[Email('Email is REQUIRED!'),
                                                     Length(min=6, max=35)])
    recaptcha = RecaptchaField()

    def validate_email(self, field):
      if User.query.filter_by(email = field.data).first():
        raise ValidationError('Email already in use.')

    def validate_username(self, field):
      if User.query.filter_by(username = field.data).first():
        raise ValidationError('Username already in use.')

class UpdateAccountForm(FlaskForm):
  username = StringField('Name', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=5, max=20, message='Must be filled')])

  email = StringField('Email Address', validators=[Email('Email is REQUIRED!'),
                                                     Length(min=6, max=35)])

  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

  def validate_email(self, email):
      if email.data != current_user.email:
        user = User.query.filter_by(username = email.data).first()
        if user:
          raise ValidationError('Email already in use.')

  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username = username.data).first()
      if user:
        raise ValidationError('Username already in use.')
    

@app.route('/')
def base():
  return render_template('base.html')


@app.route('/login', methods=['GET', 'POST']) 
def login():
  if current_user.is_authenticated:
    return redirect(url_for('base'))
  login = loginForm()

  if login.validate_on_submit():
    user = User.query.filter_by(email = format(login.email.data)).first()
    if user == None:
      flash(f'Email or password wrong', category = 'success')
    else:
      if user and bcrypt.check_password_hash(user.password, login.password.data):
        login_user(user, remember = login.remember.data)
        flash(f'Welcome {user.username}', category = 'success')
        next_page = request.args.get('next')
        if next_page:
          return redirect(next_page)
        else:
          return redirect(url_for('base'))
      else:
        flash(f'Email or password wrong', category = 'success')
  return render_template('login.html', login=login)


@app.route('/register', methods=['GET', 'POST']) 
def register():
  if current_user.is_authenticated:
    return redirect(url_for('base'))
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

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been update', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/logout')
def logout():
  logout_user()
  flash('You have been logged out')
  return redirect(url_for('base'))


def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  f_name, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

  output_size = (125, 125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)
  
  return picture_fn 


if __name__ == '__main__':
    app.run(debug=True)