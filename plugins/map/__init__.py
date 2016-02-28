import config

# # Ping
# def consider(message):
#     if config.log: print('ping considered')
#     if message['text'].endswith('ping'):
#         if config.log: print('ping triggered')
#         return 'pong'
#     else:
#         return False

# Ping
def consider(message):
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
