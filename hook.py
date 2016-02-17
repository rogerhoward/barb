#!/usr/bin/env python

import os, sys
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r
db_name = 'hookdb'
app = Flask(__name__)
log = True


def slack_log(name, request):
    if log: print('slack_log {}: {}'.format(name, request))

    # Grab every key/value from the POST and stuff it into a dict
    message = {}
    for key, value in request.form.iteritems():
        message[key] = value

    r.connect('localhost', 28015).repl()

    # Create RethinkDB table if it doesn't exist
    if name not in r.db(db_name).table_list().run():
        if log: print('table {} does not exist'.format(name))
        r.db(db_name).table_create(name)
        r.db(db_name).table(name).index_create('timestamp').run(conn)
        r.db(db_name).table(name).index_create('channel_name').run(conn)

    # Insert message into table <name>
    if log: print('Inserting...')
    response = r.db(db_name).table(name).insert(message).run()
    return response


# Basic hook handler
@app.route('/slack/<name>', methods=['POST'])
def hook(name):
    if log: print('hook({})'.format(name))
    return jsonify(slack_log(name, request))


@app.after_request
def add_header(response):
    # Force upstream caches to refresh at 100 minute intervals
    response.cache_control.max_age = 100
    # Enable CORS to allow cross-domain loading of tilesets from this server
    # Especially useful for SeaDragon viewers running locally
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    
    app.run(processes=3, host='0.0.0.0')