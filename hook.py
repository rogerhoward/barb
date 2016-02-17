#!/usr/bin/env python

import os, sys
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

app = Flask(__name__)


# Basic hook handler
@app.route('/slack/<name>', methods=['GET', 'POST'])
def hook(name):
if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()


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