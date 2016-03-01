import config


# Whoami plugin
def consider(message):
    """Whoami: returns the askers username.

    Return: String containing a username, or False.
    """
    if config.log: print('whoami considered')
    if 'whoami' in message['text']:
        if config.log: print('whoami triggered')
        return 'you are {}'.format(message['user_name'])
    else:
        return False