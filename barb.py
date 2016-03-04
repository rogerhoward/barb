#!/usr/bin/env python

import json, os, sys, git
import bot, logger
import config
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

app = Flask(__name__)


# Channel-specific logging
@app.route('/deploy', methods=['POST'])
def deploy():
    """Receives Github hooks and deploys if a merge to master

    Args:
        request (object): the Flask request object, including the the form-
             encoded message fields which Slack POSTs

    Returns:
        bool: True, or HTTP 500.
    """

    if config.log: print('deploy()')
    g = git.cmd.Git(config.project_directory)
    g.pull()
    return jsonify({'text':'deployed'})

# Channel-specific logging
@app.route('/log', methods=['POST'])
def log():
    """Receives a Slack channel message and passes it off to slack_log()

    Args:
        request (object): the Flask request object, including the the form-
             encoded message fields which Slack POSTs

    Returns:
        bool: True, or HTTP 500.
    """
    if config.log: print('log()')
    if logger.save(request):
        return jsonify({'text':''})
    else:
        if config.log: print('log() failed')
        abort(500)


@app.route('/bot', methods=['POST'])
def bot_handler():
    """Receives a Slack bot message and tries it with each plugin.

    Args:
        request (object): the Flask request object, including the the form-
             encoded message fields which Slack POSTs

    Returns:
        bool: JSON-encoded result object if successful, 500 if auth fails, 509 if no match.
    """
    response = bot.listen(request)

    if response:
        return jsonify({'text': json.dumps(response)})
    else:
        abort(509)


# Basic root handler, because
@app.route('/')
def root():
    """Handles the root path

    Returns:
        HTTP 418: I am a teapot.
    """
    # I'm a teapot
    if config.log: print('abort 418: I am a teapot')
    abort(418)


if __name__ == '__main__':
    app.run(debug=config.debug, host='0.0.0.0', port=5000)