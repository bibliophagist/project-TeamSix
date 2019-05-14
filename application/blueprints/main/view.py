#!/usr/bin/env python
# coding: utf-8
from flask import request, Blueprint, abort, current_app as app, make_response, \
    render_template, redirect, flash
from application.request.request import Request
from application.request.request_type import RequestType
from sqlalchemy.sql.expression import func
from application.db import db

main_view = Blueprint('main_view', __name__)


@main_view.route("/random_paper", methods=['GET'])
def random_paper():
    name = "Get random paper request"
    app.logger.info(name)

    our_request = Request(RequestType.GET_RANDOM_PAPER)
    app.config['MEMORY'].append(our_request)

    from application.db.Articles import Articles
    article = db.get_db().session.query(Articles).order_by(
        func.random()).first()

    return render_template('forms/random_article.html',
                           authors=article.authors,
                           title=article.title, key_words=article.key_words,
                           abstract=article.annotation, ref=article.ref)


@main_view.route("/get_paper", methods=('GET', 'POST'))
def get_paper():
    if request.method == 'POST':
        name = "Get paper request"
        app.logger.info(name)
        title = request.form['title']
        error = None
        if not title:
            app.logger.debug('Parameter incorrect for %s', name)
            error = 'Parameter incorrect for ' + name

        our_request = Request(RequestType.GET_PAPER, title=title)
        app.config['MEMORY'].append(our_request)

        from application.db.Articles import Articles
        article = db.get_db().session.query(Articles).filter_by(
            title=our_request.title).first()
        if not article:
            error = 'Such article does not exist'
        if error is None:
            return render_template('forms/get_article.html', output=True,
                                   authors=article.authors,
                                   title=article.title,
                                   key_words=article.key_words,
                                   abstract=article.annotation,
                                   ref=article.ref)
        flash(error)
    return render_template('forms/get_article.html', output=False)


@main_view.route("/find_paper", methods=['POST'])
def find_similar_paper():
    name = 'Find similar paper request'
    app.logger.info(name)
    data = request.json
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    our_request = Request(RequestType.FIND_SIMILAR_PAPER, data.get('Authors'),
                          data.get('Title'), data.get('Key words'),
                          data.get('Annotation'))
    if not (
            our_request.authors and our_request.title and our_request.key_words
            and our_request.annotation):
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    app.config['MEMORY'].append(our_request)

    # TODO implement request handler
    response = 'Some response from handler to request'

    return name + ':' + response


@main_view.route("/add_paper", methods=('GET', 'POST'))
def add_paper():
    if request.method == 'POST':
        name = 'Add paper to DB request'
        app.logger.info(name)
        authors = request.form['authors']
        title = request.form['title']
        key_words = request.form['key_words']
        abstract = request.form['abstract']
        ref = request.form['ref']
        error = None
        if not (authors or title or key_words or abstract or ref):
            app.logger.debug('Arguments incorrect for %s', name)
            error = 'One or more arguments are missing.'
        our_request = Request(RequestType.ADD_PAPER, authors,
                              title, key_words,
                              abstract, ref)
        app.config['MEMORY'].append(our_request)

        if error is None:
            from application.db.Articles import Articles
            if not db.get_db().session.query(Articles).filter_by(
                    title=our_request.title).first():
                articles = Articles(our_request.title, our_request.authors,
                                    our_request.key_words,
                                    our_request.annotation,
                                    our_request.ref)
                db.get_db().session.add(articles)
                db.get_db().session.commit()
                response = 'was handled successfully'
            else:
                response = 'was handled unsuccessfully: ' \
                           'Such article already exists'
            flash(name + ' ' + response)
        else:
            flash(error)
    return render_template('forms/add_article.html')


@main_view.route("/update_paper", methods=('GET', 'POST'))
def update_paper():
    if request.method == 'POST':
        name = 'Update paper DB request'
        app.logger.info(name)
        authors = request.form['authors']
        title = request.form['title']
        key_words = request.form['key_words']
        abstract = request.form['abstract']
        ref = request.form['ref']
        error = None
        if not (authors or title or key_words or abstract or ref):
            app.logger.debug('Arguments incorrect for %s', name)
            error = 'One or more arguments are missing.'
        our_request = Request(RequestType.UPDATE_PAPER, authors,
                              title, key_words,
                              abstract, ref)

        app.config['MEMORY'].append(our_request)
        if error is None:
            from application.db.Articles import Articles
            if db.get_db().session.query(Articles).filter_by(
                    title=our_request.title).first():
                db.get_db().session.query(Articles).filter(
                    Articles.title == our_request.title).update(
                    {'annotation': our_request.annotation,
                     'authors': our_request.authors,
                     'key_words': our_request.key_words,
                     'ref': our_request.ref})
                db.get_db().session.commit()
                response = 'was handled successfully'
            else:
                response = 'was handled unsuccessfully:' \
                           ' Such article does not exists'
            flash(name + ' ' + response)
        else:
            flash(error)
    return render_template('forms/update_article.html')


@main_view.route("/delete_paper", methods=('GET', 'POST'))
def delete_paper():
    if request.method == 'POST':
        name = 'Delete paper from DB request'
        app.logger.info(name)
        title = request.form['title']
        error = None
        if not title:
            app.logger.debug('Arguments incorrect for %s', name)
            error = 'Arguments are missing.'
        our_request = Request(RequestType.DELETE_PAPER, title=title)
        app.config['MEMORY'].append(our_request)

        if error is None:
            from application.db.Articles import Articles
            if db.get_db().session.query(Articles).filter_by(
                    title=our_request.title).first():
                article = db.get_db().session.query(Articles).filter_by(
                    title=title).first()
                db.get_db().session.delete(article)
                db.get_db().session.commit()
                response = 'was handled successfully'
            else:
                response = 'was handled unsuccessfully: ' \
                           'Such article dose not exists'
            flash(name + ' ' + response)
        else:
            flash(error)
    return render_template('forms/delete_article.html')


@main_view.route("/log_out", methods=['GET'])
def log_out():
    resp = make_response(redirect('http://127.0.0.1:5001/'))
    resp.set_cookie('auth', '', expires=0)

    return resp
