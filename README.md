# Barb

Barb is a Webhook-oriented bot written in Flask. Barb listens for Wehbook messages and makes available several services in response:

* logging channel conversations to a RethinkDB instance, with each channel getting its own table.
* a skeletal Slackbot written in Python, hacked together for easy extension.

```
./hook.py
```
