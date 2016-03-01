import json, os, sys
import config
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r


def save(request):
    """Saves Slack bot messages to RethinkDB.

    Args:
        request (object): the Flask request object, including the the form-
             encoded message fields which Slack POSTs

    Returns:
        bool: result object if successful, False otherwise.
    """

    if config.log: print('listening...')

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