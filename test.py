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
        shutil.copyfile("conf/accounts.json.dist", "conf/accounts.json")
        shutil.copyfile("conf/spamcan.json.dist", "conf/spamcan.json")

    def tearDown(self):
        pass

    def test_database(self):
        self.db = database.Database()
        # TODO: Extend
        self.assert_(1 == 1)

    def test_pop_server(self):
        server = pop_server.pop_server()
        t = threading.Thread(target=server.serve_forever)
        t.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(("localhost", 8088))
            received = sock.recv(1024)
            sock.sendall("QUIT foobar" + "\n")
        finally:
            sock.close()
        server.shutdown()
        t.join()
        self.assert_(received == "+OK SpamCan test server ready" + "\r\n")


if __name__ == "__main__":
    nose.run()
