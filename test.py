import nose
import unittest
import os
import shutil

import database


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        paths = ["data/", ]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        shutil.copyfile("conf/accounts.json.dist", "conf/accounts.json")
        shutil.copyfile("conf/spamcan.json.dist", "conf/spamcan.json")

    def tearDown(self):
        pass

    def test_a(self):
        self.db = database.Database()
        self.assert_(1 == 1)


if __name__ == "__main__":
    nose.run()
