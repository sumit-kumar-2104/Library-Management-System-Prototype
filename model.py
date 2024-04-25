from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # Define relationship with book_requests
    book_requests = db.relationship("BookRequests", back_populates="user", cascade="all, delete-orphan")
    # Define relationship with access_control
    access_controls = db.relationship("AccessControl", back_populates="user", cascade="all, delete-orphan")

class Sections(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date)
    description = db.Column(db.String)
    # Define relationship with books
    books = db.relationship("Books", back_populates="section")

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)
    author = db.Column(db.String)
    cover = db.Column(db.String)
    section = db.relationship("Sections", back_populates="books")
    book_requests = db.relationship("BookRequests", back_populates="book")
    access_controls = db.relationship("AccessControl", back_populates="book")

class BookRequests(db.Model):
    __tablename__ = "book_requests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    request_date = db.Column(db.Date)
    date_issued = db.Column(db.Date)  # Date book was issued
    return_date = db.Column(db.Date)  # Date book should be returned
    status = db.Column(db.String)
    user = db.relationship("Users", back_populates="book_requests")
    book = db.relationship("Books", back_populates="book_requests")




class AccessControl(db.Model):
    __tablename__ = "access_control"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    access_type = db.Column(db.String)  # e.g., Read, Write
    # Define relationship with users
    user = db.relationship("Users", back_populates="access_controls")
    # Define relationship with books
    book = db.relationship("Books", back_populates="access_controls")
