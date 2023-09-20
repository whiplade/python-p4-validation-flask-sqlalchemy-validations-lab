from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required!")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number != 10:
            raise ValueError("Phone Number must be 10 digits!")
        return phone_number
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

    @validates('content')
    def validate_content(self, key, content):
        if len(content) <= 250:
            raise ValueError("Hey there, Content must be at least 250 characters long!")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("Hey there, Summary must not be more than 250 characters long!")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Non-Fiction', 'Fiction']  
        if category not in valid_categories:
            raise ValueError('Category is invalid!')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        required_phrases = ["Won't Believe", "Secret", "Guess"]
        top_phrase_pattern = re.compile(r'^Top \d+$', re.IGNORECASE)

        for phrase in required_phrases:
            if phrase.lower() not in title.lower():
                raise ValueError(f'Title must contain the phrase "{phrase}".')

        if not top_phrase_pattern.match(title):
            raise ValueError('Title must match the pattern "Top [number]".')

        return title