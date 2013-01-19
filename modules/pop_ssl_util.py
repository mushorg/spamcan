import poplib


class POPUtil(object):

    def __init__(self):
        pass

    def pop_connect(self, user_name, password, hostname):
        self.M = poplib.POP3_SSL(hostname)
        self.M.set_debuglevel(0)
        self.M.user(user_name)
        self.M.pass_(password)
        print self.M.getwelcome()

    def get_stats(self):
        return self.M.stat()


if __name__ == "__main__":
    pop_connection = POPUtil("user_name", "password", "hostname")
    pop_connection.get_stats()
