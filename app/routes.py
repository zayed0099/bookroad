from flask import redirect, url_for, render_template, request, session
from app import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignInForm, LoginForm, BookQueryForm

def setup_routes():
	
	@app.route("/home")
	def home():
		return render_template('home.html')

	@app.route("/signin", methods=["GET", "POST"])

	