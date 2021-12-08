# SpamCan ![test](https://github.com/mushorg/spamcan/actions/workflows/test.yml/badge.svg)

SpamCan is a spam trap management framework. Main purpose is to manage your accounts and manage back-ground processing.


## Set-up

Requirements: See requirements.txt

Rename accounts.json.dist to accounts.json and spamcan.cfg.dist to spamcan.cfg

Replace the dummy data in accounts.json with your accounts (one per line, for line comments use a #).


## Running SpamCan

SpamCan uses ElasticSearch to parse and store spam. Before you run SpamCan make sure you have an ES instance running.
Run `python spamcan.py` and point your browser to `http:\\localhost:8000`


## TODO

- Integrate with [Thug](https://github.com/buffer/thug) honeyclient
- Integrate with [Cuckoo Sandbox](https://www.cuckoosandbox.org/) or [Malwr](http://malwr.com/) 
- Better analysis of spam messages (e.g frequent keywords, correlate URLs)
