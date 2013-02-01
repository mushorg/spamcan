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

    def test_database(self):
        paths = ["data/", ]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        configs = ["conf/accounts.json", "conf/spamcan.json"]
        for conf in configs:
            if not os.path.exists(conf):
                shutil.copyfile(conf + ".dist", conf)
        self.db = database.Database()
        # TODO: Extend
        self.assert_(1 == 1)


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
                          "protocol": "pop",
                          "hostname": "localhost:8088",
                          "smtp_host": "localhost"
                          }
        account = database.Account(account_config)
        mail_handler = mail_util.MailUtil()
        protocol_handler = mail_handler.request(account)
        count = protocol_handler.get_stats()
        protocol_handler.disconnect()
        self.assert_(count == 1)


if __name__ == "__main__":
    nose_conf = nose.config.Config()
    nose_conf.verbosity = 3
    nose.run(config=nose_conf)
