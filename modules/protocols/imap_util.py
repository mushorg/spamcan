import imaplib
import email
import ssl

class IMAPUtil(object):
    def __init__(self):
        pass

    def imap_connect(self, user_name, password, hostname, secure=True, keyfile=None, certfile=None):
        if ":" in hostname:
            host, port = hostname.split(":", 1)
            port = int(port)
            if secure:
                self.mail = imaplib.IMAP4_SSL(host, port, keyfile, certfile)
            else:
                self.mail = imaplib.IMAP4(host, port)
        else:
            if secure:
                port = 993
                self.mail = imaplib.IMAP4_SSL(hostname, port, keyfile, certfile)
            else:
                self.mail = imaplib.IMAP4(hostname)
        self.mail.login(user_name, password)

    def get_stats(self):
        data = self.mail.select('Inbox')[1]
        return int(data[0])

    def fetch_mails(self, mdir):
        remote_count = self.get_stats()
        local_count = mdir.count_local_mails()
        for num in range(local_count + 1, remote_count + 1):
            _typ, msg_data = self.mail.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    mdir.add_mail(msg)

    def disconnect(self):
        self.mail.close()
        self.mail.logout()
