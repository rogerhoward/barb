#!/usr/bin/env python

import json, os, sys
import config, plugin_manager
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

all_modules = plugin_manager.load()
app = Flask(__name__)


def slack_log(name, request):
    """Logs a Slack message object to RethinkDB.
    Depends on 'import config'
    Depends on 'import rethinkdb as r'

    Return: True or False.
    """
    if config.log: print('slack_log {}: {}'.format(name, request))

    # Grab every key/value from the POST and stuff it into a dict
    message = {}
    for key, value in request.form.items():
        message[key] = value

    # Create RethinkDB table if it doesn't exist
    if name not in r.db(config.db_name).table_list().run():
        if config.log: print('table {} does not exist'.format(name))
        r.db(config.db_name).table_create(name)
        r.db(config.db_name).table(name).index_create('timestamp').run(conn)
        r.db(config.db_name).table(name).index_create('channel_name').run(conn)

    # Insert message into table <name>
    if config.log: print('Inserting...')
    response = r.db(config.db_name).table(name).insert(message).run()

    return True


# Basic hook handler
@app.route('/log/<name>', methods=['POST'])
def hook(name):
    """Receives a Slack channel message and passes it off to slack_log()

    Return: True or 500.
    """
    if config.log: print('hook({})'.format(name))
    if slack_log(name, request):
        return True
    else:
        if config.log: print('hook({}) failed'.format(name))
        abort(500)

@app.route('/bot', methods=['POST'])
def bot():
    """Receives a Slack bot message and tries it with each plugin

    Return: Slack reponse, 500 if auth fails, 509 if no match.
    """
    if config.log: print('bot listening...')

    # Grab every key/value from the POST and stuff it into a dict
    message = {}
    for key, value in request.form.items():
        message[key] = value

    # Token check, unless in debugging mode
    if (message['token'] not in config.tokens) and not config.debug:
        if config.log: print('abort 500: token is not familiar')
        abort(500)

    # Try each module in order, by calling its consider() method
    # If trueish, it's a match and the return value is stuffed into
    # the message property of a dict, JSON encoded and sent home.
    for this_action in all_modules:
        result = this_action.consider(message)
        if result:
            return jsonify({'message': result})
        else:
            pass

    # If no match is found, just meh
    if config.log: print('abort 509: considered and ignored')
    abort(509)


# Basic root handler, because
@app.route('/')
def root():
    # I'm a teapot
    if config.log: print('abort 418: I am a teapot')
    abort(418)


@app.after_request
def add_header(response):
    # Force upstream caches to refresh at 100 minute intervals
    response.cache_control.max_age = 100
    # Enable CORS to allow cross-domain loading of tilesets from this server
    # Especially useful for SeaDragon viewers running locally
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    r.connect('localhost', 28015).repl()
    app.run(debug=config.debug, host='0.0.0.0')