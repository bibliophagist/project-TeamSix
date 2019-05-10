#!/usr/bin/env python
# coding: utf-8
from flask import request, Blueprint, abort, current_app as app
from application.db import db

main_view = Blueprint('main_view', __name__)


@main_view.route("/login", methods=['POST'])
def login():
    data = request.json
    name = 'login user' + data['username']
    app.logger.info(name)
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    from authorization.db.Users import Users
    user = db.get_db().session.query(Users).filter_by(
        username=data['username']).first()
    if not user:
        return 'Incorrect password or username!'
    if data['password'] == user.password:
        return 'User ' + user.username + ' was successfully authorized'
    return 'Incorrect password or username!'


@main_view.route("/register", methods=['POST'])
def register():
    data = request.json
    name = 'register user' + data['username']
    app.logger.info(name)
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    from authorization.db.Users import Users
    user = db.get_db().session.query(Users).filter_by(
        username=data['username']).first()
    if user:
        return 'Incorrect password or username!'
    user = Users(data['username'], data['password'])
    db.get_db().session.add(user)
    db.get_db().session.commit()
    return 'User ' + user.username + ' was successfully registered'


@main_view.route("/user_info", methods=['POST'])
def get_user_info():
    name = "Get user info request"
    app.logger.info(name)
    username = request.args.get('username')
    if not username:
        app.logger.debug('Parameter incorrect for %s', name)
        return abort(400)

    from authorization.db.Users import Users
    user = db.get_db().session.query(Users).filter_by(
        username=username).first()
    return str(user)
