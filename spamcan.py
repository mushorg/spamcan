import os
import json

from wsgiref.simple_server import make_server

import bottle
from bottle import Bottle, static_file, request, redirect
from jinja2 import Environment, FileSystemLoader

import database
from modules import mail_util, maildir_utils, mail_parser


for path in ["data/", "data/files"]:
    if not os.path.exists(path):
        os.makedirs(path)

bottle.debug(True)
app = Bottle()
template_env = Environment(loader=FileSystemLoader("./templates"))

db = database.Database()
mdir = maildir_utils.MaildirUtil()
mail_handler = mail_util.MailUtil()

accounts = db.fetch_all()


def get_account_stats(account):
    protocol_handler = mail_handler.request(account)
    if protocol_handler:
        account.remote_count = protocol_handler.get_stats()
        protocol_handler.disconnect()
    else:
        raise Exception("Invalid account: {0}".format(account))


for account in accounts:
    get_account_stats(account)


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/favicon.ico')
def favicon():
    return static_file('/favicon.ico', root='./static')


@app.route('/get_stats', method='POST')
def get_stats_button():
    account_id = request.forms.get('id')
    account = db.fetch_by_id(account_id)
    get_account_stats(account)
    return str(account.remote_count)


@app.route('/fetch_mails', method='POST')
def fetch_mails_button():
    res_dict = {}
    account_id_list = json.loads(request.forms.get('ids'))
    accounts = db.fetch_by_id_list(account_id_list)
    for account in accounts:
        mdir.create_mailbox(account.user_name)
        protocol_handler = mail_handler.request(account)
        if not protocol_handler:
            raise Exception("Invalid account: {0}".format(account))
        protocol_handler.fetch_mails(mdir)
        protocol_handler.disconnect()
        res_dict[account.account_id] = mdir.count_local_mails()
        account.mailbox_count = res_dict[account.account_id]
        mdir.mbox.close()
    db.session.commit()
    return json.dumps(res_dict)


@app.route('/crawl_mails', method='POST')
def crawl_urls_button():
    res_dict = {}
    parser = mail_parser.MailParser()
    account_id_list = json.loads(request.forms.get('ids'))
    for account_id in account_id_list:
        res_dict[account_id] = []
        account = db.fetch_by_id(account_id)
        mbox = mdir.select_mailbox(account.user_name)
        for key, message in mbox.iteritems():
            res_dict[account_id].extend(parser.walk(message))
    return json.dumps(res_dict)


@app.route('/delete_acc', method='POST')
def delete_acc_button():
    account_id = request.forms.get('id')
    res = db.delete_by_id(account_id)
    if res == True:
        ret = res
    else:
        ret = "Unable to delete account: {0}".format(res)
    return str(ret)


@app.route('/add_account', method='POST')
def add_account():
    error = ""
    account_config = {}
    account_config["user_name"] = request.forms.get('user_name')
    account_config["password"] = request.forms.get('password')
    account_config["hostname"] = request.forms.get('hostname')
    account_config["protocol"] = request.forms.get('protocol')
    account_config["smtp_host"] = request.forms.get('smtp_host')
    account = database.Account(account_config)
    try:
        mail_handler.request(account)
    except Exception as e:
        error = "Connection error ({0})".format(e)
    else:
        db.add_account(account_config)
    accounts = db.fetch_all()
    redirect("/?error={0}".format(error))


@app.route('/')
def spamcan_handler():
    #accounts = db.fetch_all()
    template = template_env.get_template('index.html')
    if request.query.error == "":
        request.query.error = None
    return template.render(account_list=accounts, error=request.query.error)

if __name__ == "__main__":
    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()
