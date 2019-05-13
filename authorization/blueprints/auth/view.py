#!/usr/bin/env python
# coding: utf-8
from flask import request, Blueprint, abort, current_app as app, redirect, \
    render_template, flash
from application.db import db

main_view = Blueprint('main_view', __name__)


@main_view.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = 'register user' + username
        app.logger.info(name)
        if not username or not password:
            app.logger.debug('Arguments incorrect for %s', name)
            return abort(400)

        from authorization.db.Users import Users
        user = db.get_db().session.query(Users).filter_by(
            username=username).first()
        if user:
            return 'Username is locked!'

        user = Users(username, password)
        db.get_db().session.add(user)
        db.get_db().session.commit()

        response = app.make_response(redirect('http://127.0.0.1:5000/'))
        response.set_cookie('auth', value='1')
        return response

    return render_template('auth/register.html')


@main_view.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = 'log in user' + username
        app.logger.info(name)
        if not username or not password:
            app.logger.debug('Arguments incorrect for %s', name)
            return abort(400)

        from authorization.db.Users import Users
        user = db.get_db().session.query(Users).filter_by(
            username=username).first()
        if not user:
            flash('Username not exist!')
        if password != user.password:
            flash('Incorrect password!')
        response = app.make_response(redirect('http://127.0.0.1:5000/'))
        response.set_cookie('auth', value='1')
        return response
    return render_template('auth/login.html')
