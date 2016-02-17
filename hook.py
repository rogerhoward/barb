#!/usr/bin/env python

import os, sys
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

app = Flask(__name__)


def slack_log(name, request):
    print('slack_log {}: {}'.format(name, request))
    message = {}

    for key, value in request.form.iteritems():
        message[key] = value

    print(message)
    r.connect("localhost", 28015).repl()
    response = r.db("hookdb").table(name).insert(message, conflict ="update").run()
    return True


# Basic hook handler
@app.route('/slack/<name>', methods=['POST'])
def hook(name):
    slack_log(name, request)
    return


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