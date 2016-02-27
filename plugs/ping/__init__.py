import config
# Ping
def consider(message):
    if message['text'].startswith('ping'):
        if config.log: print('ping triggered')
        return message
    else:
        return False
