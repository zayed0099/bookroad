from flask import redirect, url_for, render_template, request, session, flash, jsonify
from app import db, login_manager
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignInForm, LoginForm, BookQueryForm, BookUpdateForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Books
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
'''
* List of all html files needed
-home.html(default page) = done
-signin.html = done
-login.html = done
-dashboard.html = work in progress
-filter_update_delete.html = work in progress
-update_form.html = not started
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

    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        books = Books.query.filter_by(user_id=current_user.id).all()
        form = BookQueryForm()

        if form.validate_on_submit():
            book_title = form.book_title.data
            author = form.author.data
            status = form.status.data
            normalized = book_title.strip().lower()

            verify = Books.query.filter_by(title_normalized=normalized, user_id=current_user.id).all()

            if verify:
                flash('Book already exists')
            else:
                new_book_entry = Books(title=book_title, title_normalized=normalized, author=author, status=status, user_id=current_user.id)

                try:
                    db.session.add(new_book_entry)
                    db.session.commit()
                    flash('Book added successfully!')
                except SQLAlchemyError as e:
                    db.session.rollback()
                    return jsonify({'message': 'Invalid input'})

            return redirect(url_for('dashboard'))

        else:
            return render_template('dashboard.html', books=books, form=form)

    @app.route('/dashboard/view/', methods=['GET', 'POST'])
    @login_required
    def filter_update_delete():
        if request.method == 'POST':
            input_user = request.form.get('filter_data_query', '').strip()
            search_term = f"%{input_user}%"

            # Get all current user's books that match search text in title, author, or status
            fil_data = Books.query.join(User).filter(
                # only current users data
                Books.user_id == current_user.id,
                or_(
                Books.title_normalized.ilike(search_term),
                Books.author.ilike(search_term),
                Books.status.ilike(search_term)
                )
            ).all()

            return render_template('filter_update_delete.html', books=fil_data)

        else:
            books = Books.query.filter_by(user_id=current_user.id).all()
            return render_template('filter_update_delete.html', books=books)

    @app.route('/dashboard/update/<int:id>', methods=["GET", "POST"])
    @login_required
    def update_data(id):
        # Get one book by its id, but only if it belongs to the current user
        user_to_update = Books.query.filter(
            Books.id == id, 
            Books.user_id == current_user.id
        ).first_or_404()

        form = BookUpdateForm(obj=user_to_update)

        if form.validate_on_submit():
            user_to_update.title = form.title.data
            user_to_update.author = form.author.data
            user_to_update.status = form.status.data
            user_to_update.title_normalized = form.title.data.strip().lower()
            db.session.commit()

            books = Books.query.filter_by(user_id=current_user.id).all()

            return redirect(url_for('filter_update_delete'))
        else:
            return render_template('update_form.html', id=id, form=form)

    @app.route('/dashboard/delete/<int:id>', methods=["GET", "POST"])
    @login_required
    def delete_data(id):
        user_to_update = Books.query.filter(
            Books.id == id, 
            Books.user_id == current_user.id
        ).first_or_404()

        form = BookUpdateForm(obj=user_to_update)

        if request.method == 'POST':
            confirmation = request.form.get('confirm')

            if confirmation.strip().lower() == 'delete':
                db.session.delete(user_to_update)
                db.session.commit()
                return redirect(url_for('filter_update_delete'))

        else:
            return render_template('delete_form.html', form=form, id=id)
                
    @app.route('/user/change-password')
    @login_required
    def change_password():
    	pass