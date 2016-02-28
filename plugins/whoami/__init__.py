import config

# Digital Ocean instance lists
def consider(message):
    if config.log: print('whoami considered')
    if 'whoami' in message['text']:
        if config.log: print('whoami triggered')
        return message['user_name']
    else:
        return False