from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize the database
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    address_line1 = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'patient' or 'doctor'

    # One-to-many relationship: A user can have many blog posts
    blogs = db.relationship('Blog', backref='author', lazy=True, cascade='all, delete-orphan')


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    draft = db.Column(db.Boolean, default=False)

    # Foreign key for User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def truncated_summary(self, word_limit=15):
        """Returns a truncated version of the summary with a word limit."""
        if not self.summary:  # Handle empty summaries
            return ""
        words = self.summary.split()  # Split the summary into words
        if len(words) > word_limit:
            return ' '.join(words[:word_limit]) + '...'  # Truncate and add '...'
        return self.summary  # Return the full summary if within the limit

    def __repr__(self):
        return f"<Blog {self.title}>"
