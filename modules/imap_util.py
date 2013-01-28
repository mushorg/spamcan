import imaplib
import email


class IMAPUtil(object):
    def __init__(self):
        pass

    def imap_connect(self, user_name, password, hostname):
        self.mail = imaplib.IMAP4(hostname)
        self.mail.login(user_name, password)

    def get_stats(self):
    	print self.mail.list()
        data = self.mail.select('Inbox')[1]
        return int(data[0])

    def fetch_mails(self):
        _typ, data = self.mail.search(None, 'ALL')
        for num in data[0].split():
            _typ, msg_data = self.mail.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
