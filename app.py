import os
import re

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user, LoginManager, login_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, FileField, SelectField, SubmitField
from wtforms.fields.simple import TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import User, db, Blog
from wtforms.validators import Regexp
from wtforms import ValidationError

# Initialize the Flask app
app = Flask(__name__)

load_dotenv()

# Set the secret key for session management
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a7f5b8f8e8c9d2f3b9e1e8f9b8a8e8a2')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
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
# Initialize the upload folder for profile and blog images
app.config['UPLOAD_FOLDER_USER'] = os.path.join('static', 'images', 'user')
app.config['UPLOAD_FOLDER_BLOG'] = os.path.join('static', 'images', 'blog')

# Ensure the upload folders exist
if not os.path.exists(app.config['UPLOAD_FOLDER_USER']):
    os.makedirs(app.config['UPLOAD_FOLDER_USER'])

if not os.path.exists(app.config['UPLOAD_FOLDER_BLOG']):
    os.makedirs(app.config['UPLOAD_FOLDER_BLOG'])

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


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image')
    category = SelectField('Category', choices=[('Mental Health', 'Mental Health'),
                                                ('Heart Disease', 'Heart Disease'),
                                                ('Covid19', 'Covid19'),
                                                ('Immunization', 'Immunization')], validators=[DataRequired()])
    summary = StringField('Summary', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    draft = BooleanField('Save as Draft')


class EditBlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Category', choices=[('Mental Health', 'Mental Health'), ('Heart Disease', 'Heart Disease'), ('Covid19', 'Covid19'), ('Immunization', 'Immunization')])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(max=300)])
    content = TextAreaField('Content', validators=[DataRequired()])
    draft = BooleanField('Save as Draft')
    submit = SubmitField('Update Blog')


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
                profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER_USER'], filename))
                profile_picture_path = os.path.join('images', 'user', filename)  # Store relative path
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
    # Fetch the user data from the database
    user = db.session.get(User, current_user.id)

    # Debugging: Print user information to check if the user is fetched correctly
    if user:
        print(f"User ID: {user.id}, User Type: {user.user_type}")
    else:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))

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


@app.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    if current_user.user_type != 'Doctor':
        flash('You do not have permission to create blog posts.', 'danger')
        return redirect(url_for('dashboard'))

    form = BlogPostForm()

    if form.validate_on_submit():
        title = form.title.data
        image = form.image.data
        category = form.category.data
        summary = form.summary.data
        content = form.content.data
        draft = form.draft.data

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER_BLOG'], filename))
            image_path = os.path.join('images', 'blog', filename)  # Store relative path
        else:
            image_path = None

        # Create a new blog post
        new_blog = Blog(
            title=title,
            image=image_path,
            category=category,
            summary=summary,
            content=content,
            draft=draft,
            author=current_user
        )

        try:
            db.session.add(new_blog)
            db.session.commit()
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred: {str(e)}', 'danger')

    return render_template('create_blog.html', form=form)


@app.route('/blogs')
@login_required
def view_blogs():
    categories = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']
    selected_category = request.args.get('category')  # Get the selected category from the query parameters

    if current_user.user_type == 'Doctor':
        # Show all blogs (drafts and published) for the doctor
        query = Blog.query.filter((Blog.draft == False) | (Blog.user_id == current_user.id))
    else:
        # Non-doctor users see only published blogs
        query = Blog.query.filter_by(draft=False)

    if selected_category:  # Filter by selected category if provided
        query = query.filter_by(category=selected_category)

    blogs = query.order_by(Blog.date_posted.desc()).all()

    return render_template('view_blogs.html', blogs=blogs, categories=categories, selected_category=selected_category)


@app.route('/blog/<int:blog_id>')
@login_required
def view_blog(blog_id):

    blog = Blog.query.get_or_404(blog_id)
    return render_template('view_blog.html', blog=blog)


@app.route('/blogs/<category>')
@login_required
def view_blogs_by_category(category):
    if current_user.user_type != 'Patient':
        return redirect(url_for('view_blogs'))

    blogs = Blog.query.filter_by(category=category, draft=False).order_by(Blog.date_posted.desc()).all()
    return render_template('view_blogs.html', blogs=blogs, category=category)


@app.route('/blogs/all')
@login_required
def view_all_blogs():
    if current_user.user_type == 'Patient' or current_user.user_type == 'Doctor':
        # Fetch all blogs (published) for doctors
        blogs = Blog.query.filter_by(draft=False).order_by(Blog.date_posted.desc()).all()
        return render_template('view_blogs.html', blogs=blogs)
    else:
        return redirect(url_for('home'))


# Route to view only the doctor's own blogs
@app.route('/blogs/my')
@login_required
def view_my_blogs():
    if current_user.user_type == 'Doctor':
        # Fetch only the blogs authored by the logged-in doctor
        blogs = Blog.query.filter_by(user_id=current_user.id, draft=False).order_by(Blog.date_posted.desc()).all()
        return render_template('view_blogs.html', blogs=blogs)
    else:
        return redirect(url_for('home'))


@app.route('/draft')
@login_required
def view_draft():
    if current_user.user_type == 'Doctor':
        # Fetch only the blogs authored by the logged-in doctor
        blogs = Blog.query.filter_by(user_id=current_user.id, draft=True).order_by(Blog.date_posted.desc()).all()
        return render_template('draft_blog.html', blogs=blogs)
    else:
        return redirect(url_for('home'))


@app.route('/edit_blog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Ensure the current user is the author of the blog
    if blog.user_id != current_user.id:
        flash('You do not have permission to edit this blog.', 'danger')
        return redirect(url_for('view_my_blogs'))

    form = EditBlogForm(obj=blog)  # Populate form with current blog data

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.category = form.category.data
        blog.summary = form.summary.data
        blog.content = form.content.data
        blog.draft = form.draft.data

        # Handle the image update
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER_BLOG'], filename))
            blog.image = os.path.join('images', 'blog', filename)

        try:
            db.session.commit()
            flash('Blog updated successfully!', 'success')
            return redirect(url_for('view_my_blogs'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred: {str(e)}', 'danger')

    return render_template('edit_blog.html', form=form, blog=blog)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
