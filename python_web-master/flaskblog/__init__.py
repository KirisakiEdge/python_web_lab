from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from flask_restful import Api
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
api = Api(app)
ma = Marshmallow(app)

import flaskblog.forms as views

admin = Admin(app, index_view=views.MyAdminIndexView())
admin.add_view(views.UserAdminView(views.User, db.session))

import flaskblog.routes as r
api.add_resource(r.GetPosts, '/api/posts')
api.add_resource(r.GetPost, '/api/post/<string:title>')

from flaskblog import routes