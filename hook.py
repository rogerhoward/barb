#!/usr/bin/env python

import os, sys
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

app = Flask(__name__)


def slack_log(name, request):

    message = {}
    message['token'] = request.form['token']
    message['team_id'] = request.form['team_id']
    message['team_domain'] = request.form['team_domain']
    message['channel_id'] = request.form['channel_id']
    message['channel_name'] = request.form['channel_name']
    message['timestamp'] = request.form['timestamp']
    message['user_id'] = request.form['user_id']
    message['user_name'] = request.form['user_name']
    message['text'] = request.form['text']
    message['trigger_word'] = request.form['trigger_word']

    response = r.db("hookdb").table(name).insert(message, conflict ="update").run()

    print(request.form['text'])

# Basic hook handler
@app.route('/slack/<name>', methods=['GET', 'POST'])
def hook(name):
    if request.method == 'POST':
            slack_log(name, request)
    else:
        print('Sorry, {} is not supported by this endpoint'.format(request.method))


@app.after_request
def add_header(response):
    # Force upstream caches to refresh at 100 minute intervals
    response.cache_control.max_age = 100
    # Enable CORS to allow cross-domain loading of tilesets from this server
    # Especially useful for SeaDragon viewers running locally
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    r.connect("localhost", 28015).repl()
    app.run(processes=3, host='0.0.0.0')