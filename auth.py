from functools import wraps
import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.wrappers.response import Response
from models import User
from peewee import IntegrityError

auth_bp = Blueprint("auth", __name__, "/auth")

@auth_bp.route("/register", methods=('GET', 'POST'))
def register() -> Response | str:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        if not username:
            error = "username required"
        elif not password:
            error = "password required"
        
        if error is None:
            try:
                User.create(username=username, password=password)
            except IntegrityError:
                error = "username already in use"
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)
    return render_template('auth/register.jinja')

@auth_bp.route("/login", methods=('GET', 'POST'))
def login() -> Response | str:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = None
        try:
            user = User.get(User.username == username)
        except IndexError:
            error = "user does not exist"
        else:
            if user.password != password:
                error = "wrong password"

        if error is None:
            session.clear()
            session['user_id'] = user.id # pyright: ignore
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.jinja')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Login required")
            return redirect(url_for("auth.login"))
        return view(**kwargs)

def get_username_from_id(id: int) -> str:
    return User.get_by_id(id).username
