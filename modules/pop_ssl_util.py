import poplib


class POPSUtil(object):
    def __init__(self):
        pass

    def pops_connect(self, user_name, password, hostname):
        self.M = poplib.POP3_SSL(hostname)
        self.M.set_debuglevel(0)
        self.M.user(user_name)
        self.M.pass_(password)
        print self.M.getwelcome()

    def get_stats(self):
        return self.M.stat()


if __name__ == "__main__":
    pops_connection = POPSUtil("user_name", "password", "hostname")
    pops_connection.get_stats()
