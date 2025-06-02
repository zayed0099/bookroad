from flask import redirect, url_for, render_template, request, session, flash, jsonify
from app import db, login_manager
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignInForm, LoginForm, BookQueryForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Books
'''
* List of all html files needed
-home.html(default page) = done
-signin.html = done
-login.html = done
-dashboard.html = work in progress  
'''

def setup_routes(app):
    @app.route("/")
    def home():
        return render_template('home.html')

    @app.route("/signin", methods=["GET", "POST"])
    def signin():
        form = SignInForm()
        
        if form.validate_on_submit():
            username = form.username.data
            password_txt = form.password.data 
            email = form.email.data

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                flash('User already exists.')
                return redirect(url_for('login'))
            else:
                hashed_pw = generate_password_hash(password_txt)

                new_user_entry = User(username=username, email=email, password=hashed_pw)
                
                try:
                    db.session.add(new_user_entry)
                    db.session.commit()
                    flash('User registered successfully! Please Login now to access your account.')
                except SQLAlchemyError as e:
                    db.session.rollback()
                    return jsonify({'message': 'Invalid input'})

                return redirect(url_for('login'))
        
        else:
            return render_template('signin.html', form=form)

    @app.route('/login', methods=["GET", "POST"])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password_txt = form.password.data

            verify_user = User.query.filter_by(email=email).first()

            if verify_user and check_password_hash(verify_user.password, password_txt):
                login_user(verify_user)
                return(redirect(url_for('dashboard')))
            else:
                flash("We couldn't log you in. Please double-check your login details")
                return render_template('login.html', form=form)
                
        else:
            return render_template('login.html', form=form)

    @app.route('/logout')   # A simple function to logout user
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        books = Books.query.filter_by(user_id=current_user.id)
        if request.method == 'POST':
            pass
        else:
            return render_template('dashboard.html', books=books)

    @app.route('/dashbaord/view/')
    @login_required
    def view_all():
        pass
