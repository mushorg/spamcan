import nose
import unittest
import os
import shutil
import threading
import socket
import time

import database

from testing import pop_server
from modules import mail_util


class SpamCanDBTest(unittest.TestCase):

    def setUp(self):
        paths = ["data-test/", "data-test/files"]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        configs = ["conf/accounts.json", "conf/spamcan.json"]
        for conf in configs:
            if not os.path.exists(conf):
                shutil.copyfile(conf + ".dist", conf + ".test")

    def tearDown(self):
        self.db.session.close()
        os.unlink("data-test/spamcan.db.test")
        shutil.rmtree("data-test")
        configs = ["conf/accounts.json.test", "conf/spamcan.json.test"]
        for conf in configs:
            if os.path.exists(conf):
                os.unlink(conf)

    def test_database(self):
        self.db = database.Database(db_test="sqlite:///data-test/spamcan.db.test")
        accounts = self.db.fetch_all()
        print len([acc for acc in accounts])
        self.assert_(len([acc for acc in accounts]) == 3)


class SpamCanPOPTest(unittest.TestCase):

    def setUp(self):
        paths = ["data/", ]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        configs = ["conf/accounts.json", "conf/spamcan.json"]
        for conf in configs:
            if not os.path.exists(conf):
                shutil.copyfile(conf + ".dist", conf)
        self.server = pop_server.pop_server(8088)
        self.t = threading.Thread(target=self.server.serve_forever)
        self.t.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.socket.close()
        self.t.join()
        time.sleep(1)

    def test_pop_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(("localhost", 8088))
            received = sock.recv(1024)
            sock.sendall("QUIT foobar" + "\n")
        finally:
            sock.close()
        self.assert_(received == "+OK SpamCan test server ready" + "\r\n")

    def test_pop_client(self):
        account_config = {
                          "user_name": "foo@localhost",
                          "password": "foobar",
                          "protocol": "pop3",
                          "hostname": "localhost:8088",
                          "smtp_host": "localhost"
                          }
        account = database.Account(account_config)
        mail_handler = mail_util.MailUtil()
        protocol_handler = mail_handler.request(account)
        count = protocol_handler.get_stats()
        protocol_handler.disconnect()
        self.assert_(count == 1)

    def test_get_stats_method(self):
        mail_handler = mail_util.MailUtil()
        self.db = database.Database()
        account = self.db.fetch_by_id(1)
        protocol_handler = mail_handler.request(account)
        if protocol_handler:
            account.remote_count = protocol_handler.get_stats()
            protocol_handler.disconnect()
        self.assert_(account.remote_count == 1)


if __name__ == "__main__":
    nose_conf = nose.config.Config()
    nose_conf.verbosity = 3
    nose.main(config=nose_conf)
