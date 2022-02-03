from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from datetime import timedelta

app = Flask(__name__)


# Configuration για τα Secret Key, WTF CSRF Secret Key, SQLAlchemy Database URL,
# Το όνομα του αρχείου της βάσης δεδομένων θα πρέπει να είναι 'flask_movies_database.db'


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['WTF_CSRF_SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_movies_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)

### Αρχικοποίηση της Βάσης, και άλλων εργαλείων ###
### Δώστε τις σωστές τιμές παρακάτω ###

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Παρακαλώ συνδεθείτε για να δείτε αυτή τη σελίδα'


from flaskMoviesApp import routes, models
