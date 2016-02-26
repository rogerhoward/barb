# Digital Ocean instance lists
def run(message):
    if message['text'].startswith('whoami'):
        if log: print('whoami triggered')
        return message['user_name']
    else:
        return False