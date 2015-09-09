import os
import json
import email

from wsgiref.simple_server import make_server

import bottle
from bottle import Bottle, static_file, request, redirect
from jinja2 import Environment, FileSystemLoader

import database
from database import Mail
from modules import mail_util, maildir_utils, mail_parser

DEBUG = True

for path in ["data/", "data/files"]:
    if not os.path.exists(path):
        os.makedirs(path)

#enable debugging mode
bottle.debug(DEBUG)

app = Bottle()

template_env = Environment(loader=FileSystemLoader("./templates"))

db = database.Database()
mdir = maildir_utils.MaildirUtil()
mail_handler = mail_util.MailUtil()
parser = mail_parser.MailParser()

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

    user_mbox = mdir.select_mailbox(account.user_name)
    for i, (key, msg) in enumerate(user_mbox.iteritems()):
        if msg.get_subdir() == "new":
            mbody = parser.get_body(msg)
            mheaders = parser.get_headers(msg)
            subject = parser.get_subject(mheaders)
            sender = parser.get_sender(mheaders)
            mail = database.Mail(headers=mheaders, body=mbody, 
                                account_id=account.account_id,
                                subject=subject,sender=sender)
            db.session.add(mail)
      #  mdir.move_parsed(account.user_name,message[0])
            msg.set_subdir("cur")
            user_mbox[key] = msg
    db.session.commit()
    mdir.mbox.close()
    return json.dumps(res_dict)

@app.route('/crawl_mails', method='POST')
def crawl_urls_button():
    res_dict = {}
    parser = mail_parser.MailParser()
    account_id_list = json.loads(request.forms.get('ids'))
    for account_id in account_id_list:
        account = db.fetch_by_id(account_id)
        mails = db.fetch_mail_by_user(account_id)
    for mail in mails:
        body = mail.body
        for link in parser.get_urls(body):
            url = database.Url(mail_id=mail.id, url=link)
            db.session.add(url)
        db.session.commit()
    return json.dumps(res_dict)


@app.route('/delete_acc', method='POST')
def delete_acc_button():
    account_id = request.forms.get('id')
    res = db.delete_by_id(account_id)
    if res == True:
        ret = res
    else:
        ret = "Unable to delete account: {0}".format(res)
    redirect("/?error={0}".format(res))


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
        protocol_handler = mail_handler.request(account)
        protocol_handler.disconnect()
    except Exception as e:
        error = "Connection error ({0})".format(e)
    else:
        db.add_account(account_config)
    accounts = db.fetch_all()
    redirect("/?error={0}".format(error))


@app.route('/files')
def files():
    files_info = {}
    files_info["file_num"] = len(os.listdir("data/files"))
    template = template_env.get_template('files.html')
    return template.render(files_info=files_info)


@app.route('/')
def spamcan_handler():
    accounts = db.fetch_all()
    template = template_env.get_template('index.html')
    if request.query.error == "":
        request.query.error = None
    return template.render(account_list=accounts, error=request.query.error)

@app.route('/urls')
def mails():
    urls = db.fetch_urls()
    template = template_env.get_template('urls.html')
    if request.query.error == "":
        request.query.error = None
    return template.render(url_list=urls, error=request.query.error)

@app.route('/mails')
def mails():
    mails = db.fetch_mails()
    template = template_env.get_template('mails.html')
    if request.query.error == "":
        request.query.error = None
    return template.render(mail_list=mails, error=request.query.error)

@app.route('/mail/<mailId:int>')
def mail(mailId):
    mail = db.fetch_mail_by_id(mailId)
    template = template_env.get_template('mail.html')
    if request.query.error == "":
        request.query.error = None
    return template.render(mail=mail, error=request.query.error)

if __name__ == "__main__":
    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()
