import config

# Digital Ocean instance lists
def consider(message):
    if config.log: print('digitalocean list considered')
    if message['text'].startswith('dolist'):
        if config.log: print('digitalocean list triggered')
        servers = ['a', 'b', 'c', 'd']
        return ', '.join(servers)
    else:
        return False