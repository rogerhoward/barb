"""Application configuration file.

Load by 'import config', not 'from config import *'
Access properties as 'config.property'
"""

import os, json

project_directory = os.path.dirname(os.path.realpath(__file__))

plugin_directory_name = "plugins"
plugin_directory = os.path.join(project_directory, plugin_directory_name)

main_entry_point = "__init__"

tokens = ['']
db_name = 'hookdb'

log = True
debug = True

secret_path = os.path.join(os.path.dirname(os.path.dirname(project_directory)), 'secrets.json')
with open(secret_path) as secret_file:    
    secrets = json.load(secret_file)