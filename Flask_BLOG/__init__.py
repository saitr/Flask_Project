from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from Flask_BLOG.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
app = Flask(__name__)
from flask_login import LoginManager


app.config['SECRET_KEY'] = '3fde70afaf94e34e972d0ed7e78760c'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from Flask_BLOG import routes