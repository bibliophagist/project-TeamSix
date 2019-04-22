#!/usr/bin/env python
# coding: utf-8
from flask import Flask, request, Blueprint, abort, current_app as app
from homeworks.homework_06_web.request.request import Request
from homeworks.homework_06_web.request.request_type import RequestType
import logging

main_view = Blueprint('main_view', __name__)


@main_view.route("/random_paper", methods=['GET'])
def random_paper():
    name = "Get random paper request"
    app.logger.info(name)
    title = request.args.get('Title')
    if not title:
        app.logger.debug('Parameter incorrect for %s', name)
        return abort(400)

    our_request = Request(RequestType.GET_RANDOM_PAPER)
    app.config['MEMORY'].append(our_request)

    # TODO implement request handler

    return '', 204


@main_view.route("/find_paper", methods=['POST'])
def find_similar_paper():
    name = 'Find similar paper request'
    app.logger.info(name)
    data = request.json
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    our_request = Request(RequestType.FIND_SIMILAR_PAPER, data.get('Authors'), data.get('Title'), data.get('Key words'),
                          data.get('Abstract'))
    if not (our_request.authors and our_request.title and our_request.key_words and our_request.abstract):
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    app.config['MEMORY'].append(our_request)

    # TODO implement request handler
    response = 'Some response from handler to request'

    return name + ':' + response


@main_view.route("/add_paper", methods=['PATCH'])
def add_paper():
    name = 'Add paper to DB request'
    app.logger.info(name)
    data = request.json
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    our_request = Request(RequestType.ADD_PAPER, data.get('Authors'), data.get('Title'), data.get('Key words'),
                          data.get('Abstract'))
    if not (our_request.authors and our_request.title and our_request.key_words and our_request.abstract):
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    app.config['MEMORY'].append(our_request)

    # TODO implement request handler
    response = 'Some response from handler to request'

    return name + ':' + response


@main_view.route("/delete_paper", methods=['DELETE'])
def delete_paper():
    name = 'Delete paper from DB request'
    app.logger.info(name)
    title = request.args.get('Title')
    if not title:
        app.logger.debug('Parameter incorrect for %s', name)
        return abort(400)

    our_request = Request(RequestType.DELETE_PAPER)
    app.config['MEMORY'].append(our_request)

    # TODO implement request handler

    return '', 204
