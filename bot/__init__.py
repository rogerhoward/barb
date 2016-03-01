import json, os, sys
import config, plugin_manager

all_modules = plugin_manager.load()


def listen(request):
    """Processes Slack bot messages.

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
    print(message)

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
            if config.log: print('response received: {}'.format(result))
            return result
        else:
            pass

    # If no match is found, just meh
    if config.log: print('abort 509: considered and ignored')
    abort(509)