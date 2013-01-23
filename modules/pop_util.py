import poplib

from email.parser import Parser

from pprint import pprint


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
        mail_parser = Parser()
        remote_count = self.get_stats()
        local_count = mdir.count_local_mails()
        if local_count < remote_count:
            for i in range(local_count + 1, remote_count + 1):
                raw = "\n".join(self.M.retr(i)[1])
                message = mail_parser.parsestr(raw)
                mdir.add_mail(message)

    def disconnect(self):
        self.M.quit()


if __name__ == "__main__":
    pop_connection = POPUtil("user_name", "password", "hostname")
    pop_connection.get_stats()
