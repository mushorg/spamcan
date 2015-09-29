import mailbox
import os

from email.parser import Parser


class MaildirUtil(object):

    def __init__(self):
        self.mail_parser = Parser()

    def create_mailbox(self, dirname):
        directory = "maildir/" + dirname + "/"
        for folder in ["tmp", "new", "cur"]:
            if not os.path.exists(directory + folder):
                os.makedirs(directory + folder)
        self.mbox = mailbox.Maildir(directory,
                                    factory=self.mail_parser.parse,
                                    create=True)

    def select_mailbox(self, dirname):
        directory = "maildir/" + dirname + "/"
        self.mbox = mailbox.Maildir(directory,
                                    factory=None,
                                    create=False)
        return self.mbox

    def add_mail(self, message):
        self.mbox.lock()
        self.mbox.add(message)
        self.mbox.flush()

    def count_local_mails(self):
        return self.mbox.__len__()
