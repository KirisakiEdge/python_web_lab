from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import InputRequired, Length, AnyOf, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Password'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lde174UAAAAALrvXJzVdpkj_y2NnGbma2FSfMFa'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lde174UAAAAAJI2fS0UySX-20jwnAhwouh6BSEG'
app.config['Testing'] = True

Bootstrap(app)


class LoginForm(FlaskForm):
    username = StringField('Name', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=5, max=20, message='Must be filled')])

    password = PasswordField('Password', validators=[InputRequired('Password is REQUIRED!'),
                                                     AnyOf(values=[app.config['SECRET_KEY'], 'secret']),
                                                     Length(min=8, message='Must be one Uppercase letter and one number'
                                                                           ' and symbol ')])

    email = StringField('Email Address', validators=[Email('Email is REQUIRED!'),
                                                     Length(min=6, max=35)])

    gender = RadioField('Chose your gender', choices=[('male', 'man'), ('female', 'woman')],
                        validators=[InputRequired('Sex is REQUIRED!')], default='male')
    recaptcha = RecaptchaField()


@app.route('/', methods=['GET', 'POST']) #@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1> Check your data </h1>' + \
               '<h3> Your username is {}.'.format(form.username.data) + \
               '<h3> Your password is {}.'.format(form.password.data) + \
               '<h3> Your email is {}.'.format(form.email.data) + \
               '<h3> Your gender is {}.'.format(form.gender.data)
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
