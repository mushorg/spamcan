import mailbox
import os
from modules.protocols import imap_util, pop_util
from email.parser import Parser

# Handles POP3 and IMAP connections
class MailUtil(object):
    def __init__(self):
        self.imap_handler = imap_util.IMAPUtil()
        self.pop_handler = pop_util.POPUtil()

    def request(self, account):
        protocol_handler = None
        if account.protocol == "imap":
            self.imap_handler.imap_connect(
                account.user_name, account.password, account.hostname
            )
            protocol_handler = self.imap_handler
        elif account.protocol == "pop3":
            try:
                self.pop_handler.pop_connect(
                    account.user_name, account.password, account.hostname
                )
            except:
                print("Unable to connect to %s" % account.hostname)
            protocol_handler = self.pop_handler
        return protocol_handler


# Handles mailboxes
class MaildirUtil(object):
    def __init__(self):
        self.mail_parser = Parser()

    def create_mailbox(self, dirname):
        directory = "maildir/" + dirname + "/"
        for folder in ["tmp", "new", "cur"]:
            if not os.path.exists(directory + folder):
                os.makedirs(directory + folder)
        self.mbox = mailbox.Maildir(
            directory, factory=self.mail_parser.parse, create=True
        )

    def select_mailbox(self, dirname):
        directory = "maildir/" + dirname + "/"
        self.mbox = mailbox.Maildir(directory, factory=None, create=False)
        return self.mbox

    def add_mail(self, message):
        self.mbox.lock()
        self.mbox.add(message)
        self.mbox.flush()

    def count_local_mails(self):
        return self.mbox.__len__()
