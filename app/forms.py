from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

class SignInForm(FlaskForm):
	username = StringField('Enter a username', validators=[DataRequired()])
	email = StringField('Enter an Email', validators=[DataRequired(), Email()])
	password = PasswordField('Enter a strong Password', validators=[DataRequired(), Length(min=8)])
	
	submit = SubmitField('Submit')

class LoginForm(FlaskForm):
	email = StringField('Enter an Email', validators=[DataRequired(), Email()])
	password = PasswordField('Enter a strong Password', validators=[DataRequired(), Length(min=8)])
	
	submit = SubmitField('Submit')

class BookQueryForm(FlaskForm):
	book_title = StringField('Enter the Book Name.', validators=[DataRequired()])
	author = StringField('Enter the author name.', validators=[DataRequired()])
	
	choices = [('To Read', 'To Read'), ('Reading', 'Reading'), ('Read', 'Read')]
	status = SelectField('Select Status', choices=choices, validators=[DataRequired()])

	submit = SubmitField('Submit')