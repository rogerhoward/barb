import config, digitalocean

# Digital Ocean instance lists
def consider(message):
    """Lists all DigitalOcean droplets.

    Return: Array of droplet names, or False.
    """
    if config.log: print('digitalocean list considered')

    possible_trigger = '{} droplets'.format(message['trigger_word'])
    if message['text'].startswith(possible_trigger):
        if config.log: print('digitalocean list triggered')

        manager = digitalocean.Manager(token=config.secrets['do_secret'])
        servers = []
        for this_droplet in manager.get_all_droplets():
             servers.append(this_droplet.name)

        return ', '.join(servers)
    else:
        return False
