import json

from wsgiref.simple_server import make_server

from bottle import Bottle, static_file, request
from jinja2 import Environment, FileSystemLoader

import database
from modules import imap_util


app = Bottle()
template_env = Environment(loader=FileSystemLoader("./templates"))

db = database.Database()
with open("accounts.json", "rb") as account_file:
    for line in account_file:
        if line.startswith("#"):
            continue
        account_config = json.loads(line)
        db.add_account(account_config)
accounts = db.fetch()
imap_handler = imap_util.IMAPUtil(accounts[0].user_name,
                                  accounts[0].password,
                                  accounts[0].hostname)
imap_count = 0


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/favicon.ico')
def favicon():
    return static_file('/favicon.ico', root='./static')


@app.route('/stats', method='GET')
def get_stats_button():
    imap_count = imap_handler.get_stats()
    return str(imap_count)


@app.route('/')
def spamcan_handler():
    template = template_env.get_template('index.html')
    return template.render(account_list=accounts, count=imap_count)


httpd = make_server('', 8000, app)
print "Serving on port 8000..."
httpd.serve_forever()
