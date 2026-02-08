from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enpenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b773a01fe245ec113e732fce'
app.config['JWT_SECRET_KEY'] = '7901bc33269005bcbf32ca3c'
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
jwt = JWTManager(app)
cors = CORS(app,supports_credentials=True)
from expenseTracker import routes

with app.app_context():
    db.create_all()


