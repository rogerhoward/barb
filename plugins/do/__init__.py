import config

# Digital Ocean instance lists
def consider(message):
    if config.log: print('digitalocean list considered')
    if 'dolist' in message['text']:
        if config.log: print('digitalocean list triggered')
        servers = ['a', 'b', 'c', 'd']
        return ', '.join(servers)
    else:
        return False