from wsgiref.simple_server import make_server

from bottle import route, Bottle, static_file
from jinja2 import Environment, FileSystemLoader

import database


app = Bottle()
template_env = Environment(loader=FileSystemLoader("./templates"))


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')


@app.route('/favicon.ico')
def favicon():
    return static_file('/favicon.ico', root='./static')


@app.route('/')
def spamcan_handler():
    db = database.Database()
    accounts = db.fetch()
    template = template_env.get_template('spamcan.html')
    return template.render(account_list=accounts)


httpd = make_server('', 8000, app)
print "Serving on port 8000..."
httpd.serve_forever()
