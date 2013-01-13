import json

from wsgiref.simple_server import make_server

import bottle
from bottle import Bottle, static_file, request, redirect
from jinja2 import Environment, FileSystemLoader

import database
from modules import imap_util, pop_util

bottle.debug(True)

app = Bottle()
template_env = Environment(loader=FileSystemLoader("./templates"))

db = database.Database()


def acounts_from_config():
    with open("accounts.json", "rb") as account_file:
        for line in account_file:
            if line.startswith("#"):
                continue
            account_config = json.loads(line)
            db.add_account(account_config)


acounts_from_config()

imap_handler = imap_util.IMAPUtil()
pop_handler = pop_util.POPUtil()

accounts = db.fetch_all()


def get_account_stats(account):
    if account.protocol == "imap":
        imap_handler.imap_connect(account.user_name,
                                  account.password,
                                  account.hostname)
        account.count = imap_handler.get_stats()
    elif account.protocol == "pop":
        pop_handler.pop_connect(account.user_name,
                                account.password,
                                account.hostname)
        account.count = pop_handler.get_stats()


for account in accounts:
    get_account_stats(account)


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/favicon.ico')
def favicon():
    return static_file('/favicon.ico', root='./static')


@app.route('/stats', method='POST')
def get_stats_button():
    account_id = request.forms.get('id')
    account = db.fetch_by_id(account_id)
    get_account_stats(account)
    return str(account.count)


@app.route('/add_account', method='POST')
def add_account():
    account_config = {}
    account_config["user_name"] = request.forms.get('user_name')
    account_config["password"] = request.forms.get('password')
    account_config["hostname"] = request.forms.get('hostname')
    account_config["protocol"] = request.forms.get('protocol')
    account_config["smtp_host"] = request.forms.get('smtp_host')
    try:
        if account.protocol == "imap":
            imap_handler.imap_connect(account_config["user_name"],
                                      account_config["password"],
                                      account_config["hostname"])
        elif account.protocol == "pop":
            pop_handler.pop_connect(account.user_name,
                                    account.password,
                                    account.hostname)
    except Exception as e:
        error = "Connection error ({0})".format(e)
    else:
        db.add_account(account_config)
    accounts = db.fetch_all()
    redirect("/?error={0}".format(error))


@app.route('/')
def spamcan_handler():
    template = template_env.get_template('index.html')
    if request.query.error == "":
        request.query.error = None
    return template.render(account_list=accounts, error=request.query.error)


if __name__ == "__main__":
    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()
