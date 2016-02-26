#!/usr/bin/env python
import utils, config
all_modules = utils.get_modules(config.module_directory)

for this_action in all_modules:
    result = this_action.consider({'text': 'this is the message'})
    if result:
        print result
        break
    else:
        pass