import json

from wsgiref.simple_server import make_server

from bottle import route, Bottle, static_file
from jinja2 import Environment, FileSystemLoader

import database


app = Bottle()
template_env = Environment(loader=FileSystemLoader("./templates"))


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/favicon.ico')
def favicon():
    return static_file('/favicon.ico', root='./static')


@app.route('/')
def spamcan_handler():
    db = database.Database()
    with open("accounts.json", "rb") as account_file:
        for line in account_file:
            if line.startswith("#"):
                continue
            account_config = json.loads(line)
            db.add_account(account_config)
    accounts = db.fetch()
    template = template_env.get_template('spamcan.html')
    return template.render(account_list=accounts)


httpd = make_server('', 8000, app)
print "Serving on port 8000..."
httpd.serve_forever()
