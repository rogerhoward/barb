#!/usr/bin/env python

# from hook import log

# Imports all importable python modules within a directory 
# into an array of functions
def get_modules(module_directory):
    import pkgutil, sys
    modules = []
    for importer, package_name, _ in pkgutil.iter_modules([module_directory]):
        full_package_name = '%s.%s' % (module_directory, package_name)
        if full_package_name not in sys.modules:
            # if log: print('loading {}...'.format(full_package_name))
            module = importer.find_module(package_name).load_module(full_package_name)
            modules.append(module)
    return modules


from importlib import import_module
from os import path, listdir

def get_plugins():
    plugins = {}
    plugin_dir = path.join(path.dirname(__file__), 'plugins')

    import_string_list = [''.join(['.plugins.', d]) for d
                          in listdir(plugin_dir)
                          if path.isdir(path.join(plugin_dir, d))
                          and not d.startswith('__')]

    print(str(len(import_string_list)) + " imports to do...")

    for import_string in import_string_list:
        module = import_module(import_string, __package__)
        plugins.update({module.__name__.split('.')[2]: module})

    print(str(len(plugins)) + " plugins in the app")
    return plugins
