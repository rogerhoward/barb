# Digital Ocean instance lists
def run(message):
    if message['text'].startswith('dolist'):
        if log: print('digitalocean list triggered')
        servers = ['a', 'b', 'c', 'd']
        return ', '.join(servers)
    else:
        return False