import config

# Ping
def consider(message):
    """Ping: returns the entire payload Slack sends to it.
    Great for debugging Slackbots.

    Return: Dictory of original Slack payload, or False.
    """
    if config.log: print('ping considered')
    if message['text'].endswith('ping'):
        if config.log: print('ping triggered')
        return message
    else:
        return False
