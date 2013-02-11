import poplib

from email.parser import Parser


class POPUtil(object):

    def __init__(self):
        pass

    def pop_connect(self, user_name, password, hostname, ssl=False, keyfile=None, certfile=None):
        if ":" in hostname:
            host, port = hostname.split(":", 1)
            port = int(port)
            if ssl:
                self.M = poplib.POP3_SSL(host, port, keyfile, certfile)
            else:
                self.M = poplib.POP3(host, port, timeout=5)
        else:
            if ssl:
                port = 995
                self.M = poplib.POP3_SSL(hostname, port, keyfile, certfile)
            else:
                self.M = poplib.POP3(hostname, timeout=5)
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
