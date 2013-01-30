import imaplib
import email


class IMAPUtil(object):
    def __init__(self):
        pass

    def imap_connect(self, user_name, password, hostname, ssl=False, keyfile=None, certfile=None):
        if ":" in hostname:
            host, port = hostname.split(":", 1)
            port = int(port)
            if ssl:
                self.mail = imaplib.IMAP4_SSL(host, port, keyfile, certfile)
            else:
                self.mail = imaplib.IMAP4(host, port)
        else:
            if ssl:
                self.mail = imaplib.IMAP4_SSL(hostname, keyfile, certfile)
            else:
                self.mail = imaplib.IMAP4(hostname)
        self.mail.login(user_name, password)

    def get_stats(self):
        data = self.mail.select('Inbox')[1]
        return int(data[0])

    def fetch_mails(self):
        _typ, data = self.mail.search(None, 'ALL')
        for num in data[0].split():
            _typ, msg_data = self.mail.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
