import config

# Digital Ocean instance lists
def consider(message):
    if config.log: print('whoami considered')
    if message['text'].startswith('whoami'):
        if config.log: print('whoami triggered')
        return message['user_name']
    else:
        return False