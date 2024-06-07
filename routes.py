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
            return redirect(url_for('main.search_user'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@bp.route('/search', methods=['GET', 'POST'])
@auth.login_required
def search_user():
    if request.method == 'POST':
        username = request.form['username']
        query = text(f"SELECT * FROM user WHERE username = '{username}'")
        result = db.session.execute(query)
        user = result.fetchone()
        if user:
            return f"User: {user.username}, Email: {user.email}"
        else:
            return "User not found", 404
    return render_template('search.html')

@bp.route('/xss', methods=['GET', 'POST'])
def xss_vulnerability():
    if 'token' not in session or session['token'] not in tokens.values():
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        username = request.form['username']
        return render_template('xss_result.html', username=username)
    return render_template('xss.html')
