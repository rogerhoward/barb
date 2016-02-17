#!/usr/bin/env python

import requests
import dateutil.parser
from xml.etree import ElementTree
import rethinkdb as r


def update():
    print 'update() begin'

    # Connect to ReThinkDB
    r.connect("localhost", 28015).repl()

    # Get XML data from remote API and parse it
    url = 'http://api.ezaxess.com/v2/pd/longbeach/crimes/all'
    root = ElementTree.fromstring(requests.get(url).content)

    for item in root.findall('item'):
        # Construct Python dictionary from XML nodes
        incident = {
            'id': int(item.find('id').text),
            'item_id': int(item.find('id').text),
            'case_id': int(item.find('case_number').text),
            'incident_id': int(item.find('incident_id').text),
            'title': item.find('title').text.strip(),
            'description': item.find('description').text.strip(),
            'time': dateutil.parser.parse(item.find('date_occured').text),
            'address': item.find('block_address').text.strip(),
            'city': item.find('city').text.strip(),
            'state': item.find('state').text.strip(),
            'latitude': item.find('latitude').text.strip(),
            'longitude': item.find('longitude').text.strip(),
        }

        response = r.db("lbpd").table("incidents").insert(incident, conflict ="update").run()

        print(incident['id'], response["inserted"])

    print 'update() completed'


if __name__ == '__main__':
    update()
