import config

# Ping
def consider(message):
    if config.log: print('ping considered')
    if message['text'].startswith('ping'):
        if config.log: print('ping triggered')
        return message
    else:
        return False
