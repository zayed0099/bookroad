from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
    
    # One-to-many relationship: one user has many books
	books = db.relationship('Books', backref = 'user', lazy=True)

	def __repr__(self):
		return f'<email {self.email}>'

class Books(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	author = db.Column(db.String(100), unique=False, nullable=False)
	status = db.Column(db.String(10), default='Read') # Other to options are 'Reading' and 'To Read'

	# Foreign key directed to 'users.id'. Foreign Key structure - 'table_name.column_name'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	
	def __repr__(self):
		return f'<Author {self.title}>'