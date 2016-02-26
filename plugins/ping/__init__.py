# Ping
def run(message):
    if message['text'].startswith('ping'):
        if log: print('ping triggered')
        return message
    else:
        return False
