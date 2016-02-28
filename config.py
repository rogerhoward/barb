"""Application configuration file.

Load by 'import config', not 'from config import *'
Access properties as 'config.property'
"""

import os

project_directory = os.path.dirname(os.path.realpath(__file__))

plugin_directory_name = "plugins"
plugin_directory = os.path.join(project_directory, plugin_directory_name)

main_entry_point = "__init__"

tokens = ['']
db_name = 'hookdb'

log = True
debug = True