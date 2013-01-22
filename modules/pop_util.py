import poplib

from email.parser import Parser


class POPUtil(object):

    def __init__(self):
        pass

    def pop_connect(self, user_name, password, hostname):
        self.M = poplib.POP3(hostname)
        self.M.set_debuglevel(0)
        self.M.user(user_name)
        self.M.pass_(password)

    def get_stats(self):
        return self.M.stat()[0]

    def fetch_mails(self, mdir):
        for i in range(self.get_stats()):
            for j in self.M.retr(i + 1)[1]:
                message = Parser().parsestr(j)
                mdir.add_mail(message)
        return i + 1

    def disconnect(self):
        self.M.quit()


if __name__ == "__main__":
    pop_connection = POPUtil("user_name", "password", "hostname")
    pop_connection.get_stats()
