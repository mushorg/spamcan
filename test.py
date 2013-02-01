import nose
import unittest
import os
import shutil
import threading
import socket

import database
from testing import pop_server
from modules import mail_util


class SpamCanTest(unittest.TestCase):

    def setUp(self):
        paths = ["data/", ]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        configs = ["conf/accounts.json", "conf/spamcan.json"]
        for conf in configs:
            if not os.path.exists(conf):
                shutil.copyfile(conf + ".dist", conf)

    def tearDown(self):
        pass

    def test_database(self):
        self.db = database.Database()
        # TODO: Extend
        self.assert_(1 == 1)

    def test_pop_server(self):
        self.server = pop_server.pop_server(8088)
        self.t = threading.Thread(target=self.server.serve_forever)
        self.t.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(("localhost", 8088))
            received = sock.recv(1024)
            sock.sendall("QUIT foobar" + "\n")
        finally:
            sock.close()
            self.server.shutdown()
            self.t.join()
        self.assert_(received == "+OK SpamCan test server ready" + "\r\n")

    def test_pop_client(self):
        self.server = pop_server.pop_server(8089)
        self.t = threading.Thread(target=self.server.serve_forever)
        self.t.start()
        account_config = {
                          "user_name": "foo@localhost",
                          "password": "foobar",
                          "protocol": "pop",
                          "hostname": "localhost:8089",
                          "smtp_host": "localhost"
                          }
        account = database.Account(account_config)
        mail_handler = mail_util.MailUtil()
        protocol_handler = mail_handler.request(account)
        count = protocol_handler.get_stats()
        protocol_handler.disconnect()
        self.server.shutdown()
        self.t.join()
        self.assert_(count == 1)


if __name__ == "__main__":
    nose.run()
