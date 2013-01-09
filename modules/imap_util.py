import imaplib


class IMAPUtil(object):

    def imap_connect(self, user_name, password, hostname):
        self.mail = imaplib.IMAP4_SSL(hostname)
        self.mail.login(user_name, password)

    def __init__(self, user_name, password, hostname):
        self.imap_connect(user_name, password, hostname)

    def get_stats(self):
        data = self.mail.select('INBOX')[1]
        return int(data[0])
