import config


# Google Maps
def consider(message):
    """Map: returns a Google Map link to the specified location.

    Return: URL to a Google Map, or False.
    """
    if config.log: print('map considered')
    possible_trigger = '{} map '.format(message['trigger_word'])
    if message['text'].startswith(possible_trigger):
        if config.log: print('map triggered')

        map_string = message['text'][len(possible_trigger):]
        if config.log: print('map string: {}'.format(map_string))
        map_url = 'https://www.google.com/maps/place/{}'.format(map_string.replace(' ', '+'))

        return map_url
    else:
        return False
