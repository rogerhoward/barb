#!/usr/bin/env python

import json, os, sys, requests
import config, plugin_manager
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

all_modules = plugin_manager.load()

if __name__ == '__main__':
    import digitalocean
    manager = digitalocean.Manager(token=config.secrets['do_secret'])
    droplet_names = []
    for this_droplet in manager.get_all_droplets():
        droplet_names.append(this_droplet.name)
    print(droplet_names)