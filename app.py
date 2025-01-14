import os
import re
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user, LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import User, db
from wtforms.validators import Regexp
from wtforms import ValidationError

# Initialize the Flask app
app = Flask(__name__)

# Set the secret key for session management
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a7f5b8f8e8c9d2f3b9e1e8f9b8a8e8a2')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view route
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'


# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Initialize SQLAlchemy
db.init_app(app)

# Set the upload folder for profile pictures
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

# Create the upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Create all tables within app context
with app.app_context():
    db.create_all()


# Custom email validation regex
def validate_email_regex(field):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, field.data):
        raise ValidationError("Invalid email format")


# Signup
# form class
class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture')
    username = StringField('Username', validators=[DataRequired()])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message="Invalid email address"
            )
        ]
    )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(6)])
    user_type = SelectField('User Type', choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')],
                            validators=[DataRequired()])
    submit = SubmitField('Sign Up')


# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Get form data
            first_name = form.first_name.data
            last_name = form.last_name.data
            profile_picture = form.profile_picture.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            address_line1 = form.address_line1.data
            city = form.city.data
            state = form.state.data
            pincode = form.pincode.data
            user_type = form.user_type.data

            # Handle profile picture upload
            if profile_picture:
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_picture_path = os.path.join('images', filename)  # Store relative path
            else:
                profile_picture_path = None

            # Check if password and confirm password match
            if password != confirm_password:
                form.confirm_password.errors.append('Passwords do not match!')
                return render_template('signup.html', form=form)

            # Hash the password before saving
            hash_password = generate_password_hash(password)

            # Create a new user and add to the database
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture_path,
                username=username,
                email=email,
                password=hash_password,
                address_line1=address_line1,
                city=city,
                state=state,
                pincode=pincode,
                user_type=user_type
            )

            try:
                db.session.add(new_user)
                db.session.commit()  # Commit to the database
                flash('Account created successfully!', 'success')
                return redirect(url_for('login'))  # Redirect to login page
            except Exception as e:
                db.session.rollback()  # Rollback in case of error
                flash(f'Error occurred: {str(e)}', 'danger')

        else:
            flash("Form validation failed, please check your inputs.", 'danger')

    return render_template('signup.html', form=form)


# Login form class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


# Route for home
@app.route('/')
def home():
    return redirect(url_for('login'))


# Route for user dashboard (only accessible after login)
@app.route('/dashboard')
@login_required
def dashboard():
    user = db.session.get(User, current_user.id)
    return render_template('user_dashboard.html', user=user)


# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Get form data
            username = form.username.data
            password = form.password.data

            # Query the user from the database
            user = User.query.filter_by(username=username).first()

            # Check if user exists and password is correct
            if user and check_password_hash(user.password, password):
                login_user(user)  # Log the user in
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                login_error = "Login failed. Please check your username and/or password."
                return render_template('login.html', form=form, login_error=login_error)

    return render_template('login.html', form=form)


# Route to delete user
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        try:
            db.session.delete(user)  # Delete the user from the database
            db.session.commit()  # Commit the changes
            flash('User deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error occurred: {str(e)}', 'danger')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('dashboard'))  # Redirect to dashboard


# Route to logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session to log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to login page


if __name__ == '__main__':
    app.run(debug=True, port=5001)
