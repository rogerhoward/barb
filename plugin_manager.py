#!/usr/bin/env python
import os, imp, config

main_entry_point = "__init__"


def get():
    """Get list of available plugins.
    Result intended to be used by load() method, but may be useful elsewhere.

    Return: array of dictionaries representing each available plugin.
    """
    plugin_registry = []
    for i in os.listdir(config.plugin_directory):
        location = os.path.join(config.plugin_directory, i)
        if not os.path.isdir(location) or not main_entry_point + ".py" in os.listdir(location):
            continue
        info = imp.find_module(main_entry_point, [location])
        plugin_registry.append({"name": i, "info": info})
    return plugin_registry


def load():
    """Load available plugins as modules.

    Return: array of loaded modules
    """
    modules = []
    for plugin in get():
        modules.append(imp.load_source(plugin['name'], plugin['info'][1]))
    if config.log: print(modules)
    return modules


# all_plugin_files = get()
# print(all_plugin_files)

# all_plugins = load()
# print(all_plugins)