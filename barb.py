#!/usr/bin/env python

import json, os, sys
import config, plugin_manager
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

all_modules = plugin_manager.load()
app = Flask(__name__)


def slack_log(request):
    """Logs a Slack message object to RethinkDB.
    Depends on 'import config'
    Depends on 'import rethinkdb as r'

    Return: True or False.
    """
    if config.log: print('slack_log: {}'.format(request))

    # Grab every key/value from the POST and stuff it into a dict
    message = {}
    for key, value in request.form.items():
        message[key] = value

    # Set defaults
    if 'channel_name' in message:
        channel_name = message['channel_name']
        channel_name = ''.join(e for e in channel_name if e.isalnum())
    else:
        'unknown'

    if 'team_domain' in message:
        server_name = message['team_domain']
        server_name = ''.join(e for e in server_name if e.isalnum())
    else:
        'unknown'

    # Setup logging variables
    db_name = server_name
    table_name = channel_name

    # Connect to RethinkDB
    r.connect('localhost', 28015).repl()

    # Create RethinkDB database if it doesn't exist
    if db_name not in r.db_list().run():
        if config.log: print('database {} does not exist'.format(db_name))
        r.db_create(db_name).run()

    # Create RethinkDB table if it doesn't exist
    if table_name not in r.db(db_name).table_list().run():
        if config.log: print('table {} does not exist'.format(table_name))
        r.db(db_name).table_create(table_name).run()
        r.db(db_name).table(table_name).index_create('timestamp').run()
        r.db(db_name).table(table_name).index_create('channel_name').run()

    # Insert message into table <name>
    if config.log: print('Inserting...')
    response = r.db(db_name).table(table_name).insert(message).run()

    return True


# Channel-specific logging
@app.route('/log', methods=['POST'])
def log():
    """Receives a Slack channel message and passes it off to slack_log()

    Return: True or 500.
    """
    if config.log: print('log()')
    if slack_log(request):
        return True
    else:
        if config.log: print('log() failed')
        abort(500)

# # Channel-specific logging
# @app.route('/log/<name>', methods=['POST'])
# def log(name):
#     """Receives a Slack channel message and passes it off to slack_log()

#     Return: True or 500.
#     """
#     if config.log: print('hook({})'.format(name))
#     if slack_log(name, request):
#         return True
#     else:
#         if config.log: print('hook({}) failed'.format(name))
#         abort(500)

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
    """Handles the root path

    Return: 418.
    """
    # I'm a teapot
    if config.log: print('abort 418: I am a teapot')
    abort(418)


if __name__ == '__main__':
    app.run(debug=config.debug, host='0.0.0.0')