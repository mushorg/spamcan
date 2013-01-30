import nose
import unittest
import os
import shutil
import threading
import time

import database
from testing import pop_server


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
        self.assert_(1 == 1)

    def test_pop_server(self):
        server = pop_server.pop_server()
        t = threading.Thread(target=server.serve_forever)
        t.start()
        time.sleep(3)
        server.shutdown()
        t.join()

if __name__ == "__main__":
    nose.run()
