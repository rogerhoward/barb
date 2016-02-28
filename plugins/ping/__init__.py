import config

# Ping
def consider(message):
    if config.log: print('ping considered')
    if message['text'].endswith('ping'):
        if config.log: print('ping triggered')
        return 'pong'
    else:
        return False

# # Ping
# def consider(message):
#     if config.log: print('ping considered')
#     if message['text'].endswith('ping'):
#         if config.log: print('ping triggered')
#         return message
#     else:
#         return False
