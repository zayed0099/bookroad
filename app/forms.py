from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired

class SignInForm(FlaskForm):
	username = StringField('Enter a username', validators=[DataRequired()])
	email = StringField('Enter an Email', validators=[DataRequired()])
	password = PasswordField('Enter a strong Password', validators=[DataRequired()])
	
	submit = SubmitField('Submit')

class LoginForm(FlaskForm):
	email = StringField('Enter an Email', validators=[DataRequired()])
	password = PasswordField('Enter a strong Password', validators=[DataRequired()])
	
	submit = SubmitField('Submit')

class BookQueryForm(FlaskForm):
	book_title = StringField('Enter the Book Name.', validators=[DataRequired()])
	author = StringField('Enter the author name.', validators=[DataRequired()])
	
	choices = [('val1', 'To Read'), ('val2', 'Reading'), ('val3', 'Read')]
	status = SelectField('Select Status', choices=choices, validators=[DataRequired()])

	submit = SubmitField('Submit')