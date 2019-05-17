#!/usr/bin/env python
# coding: utf-8
from flask import request, Blueprint, current_app as app, make_response, \
    render_template, redirect, flash

from application.request.request import Request
from application.request.request_type import RequestType
from sqlalchemy.sql.expression import func
from application.db import db
import pandas as pd

main_view = Blueprint('main_view', __name__)


@main_view.route("/random_paper", methods=['GET'])
def random_paper():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
    name = "Get random paper request"
    app.logger.info(name)

    our_request = Request(RequestType.GET_RANDOM_PAPER)

    from application.db.Articles import Articles
    article = db.get_db().session.query(Articles).order_by(
        func.random()).first()
    __write_to_history__(our_request, str(article))

    return render_template('forms/random_article.html',
                           user=app.config['user'],
                           authors=article.authors,
                           title=article.title, key_words=article.key_words,
                           abstract=article.annotation, ref=article.ref)


@main_view.route("/get_paper", methods=('GET', 'POST'))
def get_paper():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
    if request.method == 'POST':
        name = "Get paper request"
        app.logger.info(name)
        title = request.form['title']
        error = None
        if not title:
            app.logger.debug('Parameter incorrect for %s', name)
            error = 'Parameter incorrect for ' + name

        our_request = Request(RequestType.GET_PAPER, title=title)

        from application.db.Articles import Articles
        article = db.get_db().session.query(Articles).filter_by(
            title=our_request.title).first()
        if not article:
            error = 'Such article does not exist'
        if error is None:
            __write_to_history__(our_request, str(article))
            return render_template('forms/get_article.html',
                                   user=app.config['user'],
                                   output=True,
                                   authors=article.authors,
                                   title=article.title,
                                   key_words=article.key_words,
                                   abstract=article.annotation,
                                   ref=article.ref)
        else:
            __write_to_history__(our_request, error)
        flash(error)
    return render_template('forms/get_article.html', user=app.config['user'],
                           output=False)


@main_view.route("/find_similar_paper", methods=('GET', 'POST'))
def find_similar_paper():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
    if request.method == 'POST':
        name = 'Find similar paper request'
        app.logger.info(name)
        authors = request.form['authors']
        title = request.form['title']
        key_words = request.form['key_words']
        abstract = request.form['abstract']
        ref = request.form['ref']
        error = None
        from application.db.Articles import Articles
        if not title:
            app.logger.debug('Arguments incorrect for %s', name)
            error = 'Title is missing.'
        if not authors or not key_words or not abstract or not ref:
            app.logger.info("Getting elements from bd")
            article = db.get_db().session.query(Articles).filter_by(
                title=title).first()
            if not article:
                app.logger.info('Such article is not in database '
                                'please provide all fields!')
                error = 'Such article is not in database' \
                        ' please provide all fields!'
        elif not db.get_db().session.query(Articles).filter_by(
                title=title).first():
            app.logger.debug('Arguments incorrect for %s', name)
            article = Articles(title, authors, key_words, abstract, ref)
            db.get_db().session.add(article)
            db.get_db().session.commit()
        if error is None:
            our_request = Request(RequestType.FIND_SIMILAR_PAPER,
                                  article.authors, article.title,
                                  article.key_words, article.annotation)
            pd.set_option('display.max_colwidth', -1)
            df = app.config['seeker'].find_article_by_text(
                article.title + article.annotation)
            __write_to_history__(our_request, df.title.to_string)
            columns = ['authors', 'title',
                       # 'ref',
                       'annotation', 'key_words']
            delete_columns = [column not in columns for column in df.columns]
            df = df.drop(columns=df.columns[delete_columns])
            return render_template('forms/show_history.html',
                                   user=app.config['user'], data=df)
        else:
            flash(error)
    return render_template('forms/find_similar_paper.html',
                           user=app.config['user'])


@main_view.route("/add_paper", methods=('GET', 'POST'))
def add_paper():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
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
            __write_to_history__(our_request, response)
            flash(name + ' ' + response)
        else:
            __write_to_history__(our_request, error)
            flash(error)
    return render_template('forms/add_article.html', user=app.config['user'])


@main_view.route("/update_paper", methods=('GET', 'POST'))
def update_paper():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
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
            __write_to_history__(our_request, response)
            flash(name + ' ' + response)
        else:
            __write_to_history__(our_request, error)
            flash(error)
    return render_template('forms/update_article.html',
                           user=app.config['user'])


@main_view.route("/delete_paper", methods=('GET', 'POST'))
def delete_paper():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
    if request.method == 'POST':
        name = 'Delete paper from DB request'
        app.logger.info(name)
        title = request.form['title']
        error = None
        if not title:
            app.logger.debug('Arguments incorrect for %s', name)
            error = 'Arguments are missing.'
        our_request = Request(RequestType.DELETE_PAPER, title=title)

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
            __write_to_history__(our_request, response)
            flash(name + ' ' + response)
        else:
            __write_to_history__(our_request, error)
            flash(error)
    return render_template('forms/delete_article.html',
                           user=app.config['user'])


@main_view.route("/show_history", methods=['GET'])
def show_history():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
    name = 'Show history DB request'
    app.logger.info(name)
    error = None
    our_request = Request(RequestType.SHOW_HISTORY)
    from application.db.History import History
    if db.get_db().session.query(History).first():
        df = pd.read_sql(db.get_db().session.query(History).statement,
                         app.config['SQLALCHEMY_DATABASE_URI'])
        pd.set_option('display.max_colwidth', -1)
        __write_to_history__(our_request, 'was handled successfully')
    else:
        error = 'was handled unsuccessfully: ' \
                'History is empty'
        __write_to_history__(our_request, error)
    if error is None:
        return render_template('forms/show_history.html',
                               user=app.config['user'], data=df)


@main_view.route("/log_out", methods=['GET'])
def log_out():
    resp = make_response(redirect('http://127.0.0.1:5001/'))
    resp.set_cookie('auth', '', expires=0)

    return resp


@main_view.route("/clean_history", methods=['GET'])
def clean_history():
    if 'auth' not in request.cookies:
        return redirect('http://127.0.0.1:5001/')
    name = 'clean history DB request'
    app.logger.info(name)
    our_request = Request(RequestType.CLEAN_HISTORY)
    from application.db.History import History
    db.get_db().session.query(History).delete()
    db.get_db().session.commit()
    __write_to_history__(our_request,
                         'history cleaned ')
    return render_template('index.html', user=app.config['user'])


def __write_to_history__(request_to_db, response_to_db):
    from application.db.History import History
    history = History(username=app.config['user'], request=str(request_to_db),
                      response=str(response_to_db))
    db.get_db().session.add(history)
    db.get_db().session.commit()
