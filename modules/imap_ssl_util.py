import imaplib


class IMAPUtil(object):
    def __init__(self):
        pass

    def imap_connect(self, user_name, password, hostname):
        self.mail = imaplib.IMAP4_SSL(hostname)
        self.mail.login(user_name, password)

    def get_stats(self):
    	print self.mail.list()
        data = self.mail.select('Inbox')[1]
        return int(data[0])
