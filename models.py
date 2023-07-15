"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Initialize the database
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg"

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)
    
# MODELS GO HERE
class User(db.Model):
    ''' User Model '''
    __tablename__ = 'users'

    def __repr__(self):
        '''Show info about user'''
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan, delete")


class Post(db.Model):
    """Blog post."""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    

class PostTag(db.Model):
    """PostTag Model"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag Model"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', cascade="all, delete",  backref='tags')
    
