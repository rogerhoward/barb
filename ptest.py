#!/usr/bin/env python

import os, imp

PluginFolder = "./plugs"
MainModule = "__init__"


def get():
    plugins = []
    for i in os.listdir(PluginFolder):
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins


def load():
    plugins = []
    for plugin in get():
        plugins.append(imp.load_module(MainModule, *plugin["info"]))
    return plugins


def loadPlugin(plugin):
    return 

all_plugin_files = get()
print all_plugin_files

all_plugins = load()
print all_plugins