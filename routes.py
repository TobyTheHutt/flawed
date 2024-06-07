from flask import Blueprint, request, render_template, session, redirect, url_for
from sqlalchemy import text
from models import db, User
from auth import auth, verify_password

bp = Blueprint('main', __name__)

tokens = {}

@bp.route('/')
def hello_world():
    return 'Hello, World!'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            token = f"{username}_static_token"
            tokens[username] = token
            session['token'] = token
            return redirect(url_for('main.search'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@bp.route('/search', methods=['GET', 'POST'])
@auth.login_required
def search():
    if request.method == 'POST':
        search_username = request.form.get('search_username', '')
        xss_username = request.form.get('xss_username', '')

        if search_username:
            # Intentionally introducing SQL injection vulnerability
            query = text(f"SELECT * FROM user WHERE username = '{search_username}'")
            result = db.session.execute(query)
            user = result.fetchone()
            if user:
                return f"User: {user.username}, Email: {user.email}"
            else:
                return "User not found", 404
        elif xss_username:
            return render_template('xss_result.html', username=xss_username)

    return render_template('search.html')
