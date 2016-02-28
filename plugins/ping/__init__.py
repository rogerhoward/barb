import config

# Ping
def consider(message):
    if config.log: print('ping considered')
    if 'ping' in message['text']:
        if config.log: print('ping triggered')
        return message
    else:
        return False
