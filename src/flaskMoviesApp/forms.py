from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError, Optional
from flaskMoviesApp.models import User
from flask_login import current_user

from datetime import datetime as dt

### Συμπληρώστε κάποια από τα imports που έχουν αφαιρεθεί ###


current_year = dt.now().year


''' Custom Validation function outside the form class '''


def maxImageSize(max_size=2):
    max_bytes = max_size * 1024 * 1024

    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(
                f'Το μέγεθος της εικόνας δε μπορεί να υπεβαίνει τα {max_size} MB')

    return _check_file_size


''' Validation function outside the form class '''


def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('Αυτό το email υπάρχει ήδη!')


class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                        validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό email"), validate_email])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    password2 = StringField(label="Επιβεβαίωση password",
                            validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                        Length(
                                min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                                EqualTo('password', message='Τα δύο πεδία password πρέπει να είναι τα ίδια')])

    submit = SubmitField('Εγγραφή')

    def validate_username(self, username):
        # Validator για έλεγχο ύπαρξης του user στη βάση
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Αυτό το username υπάρχει ήδη!')


class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                        validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    # Αρχείο Εικόνας, με επιτρεπόμενους τύπους εικόνων τα 'jpg', 'jpeg', 'png', και μέγιστο μέγεθος αρχείου εικόνας τα 2 MBytes, ΜΗ υποχρεωτικό πεδίο
    image = FileField('Εικόνα Προφίλ', validators=[Optional(strip_whitespace=True),
                                                   FileAllowed(['jpg', 'jpeg', 'png'],
                                                               'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg και png!'),
                                                   maxImageSize(max_size=2)])

    submit = SubmitField('Αποστολή')

    def validate_username(self, username):
        # if statement for user account update
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Αυτό το username υπάρχει ήδη!')

    def validate_email(self, email):
        # if statement for user account update
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Αυτό το email υπάρχει ήδη!')


class LoginForm(FlaskForm):

    email = StringField(label="email",
                        validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό.")])

    remember_me = BooleanField(label="Remember me")

    submit = SubmitField('Είσοδος')


class NewMovieForm(FlaskForm):
    # Τίτλος Ταινίας, υποχρεωτικό πεδίο κειμένου από 3 έως 50 χαρακτήρες και το αντίστοιχο label και μήνυμα στον validator
    title = StringField(label="Τίτλος Ταινίας", validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), Length(
        min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    # Υπόθεση Ταινίας, υποχρεωτικό πεδίο κειμένου, από 5 έως απεριόριστο αριθμό χαρακτήρων και το αντίστοιχο label και μήνυμα στον validator
    plot = TextAreaField(label="Υπόθεση Ταινίας", validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), Length(
        min=5, message="Αυτό το πεδίο πρέπει να είναι από 5 χαρακτήρες.")])

    # Αρχείο Εικόνας, με επιτρεπόμενους τύπους εικόνων τα 'jpg', 'jpeg', 'png', και μέγιστο μέγεθος αρχείου εικόνας τα 2 MBytes, ΜΗ υποχρεωτικό πεδίο
    image = FileField('Εικόνα της Ταινίας', validators=[Optional(strip_whitespace=True),
                                                        FileAllowed(['jpg', 'jpeg', 'png'],
                                                                    'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg και png!'),
                                                        maxImageSize(max_size=2)])

    # IntegerField με το έτος πρώτης προβολής της ταινίας, θα παίρνει τιμές από το 1888 έως το current_year που υπολογίζεται στην αρχή του κώδικα εδώ στο forms.py
    release_year = IntegerField(label="Έτος Πρώτης Προβολής Ταινίας", validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), NumberRange(
        min=1888, max=current_year, message="Αυτό το πεδίο πρέπει να είναι από 1888 έως το τρέχον έτος.")])

    # Βαθμολογία Ταινίας (IntegerField), υποχρεωτικό πεδίο, Αριθμητική τιμή από 1 έως 100, με τη χρήση του validator NumberRange, και με το αντίστοιχο label και μήνυμα στον validator
    rating = IntegerField(label="Βαθμολογία Ταινίας", validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), NumberRange(
        min=1, max=100, message="Αυτό το πεδίο πρέπει να είναι από 1 έως 100.")])

    submit = SubmitField(label='Αποστολή')
