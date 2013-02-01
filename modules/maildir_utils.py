import mailbox
import os


class MaildirUtil(object):

    def __init__(self):
        pass

    def create_mailbox(self, dirname):
        directory = "maildir/" + dirname + "/"
        for folder in ["tmp", "new", "cur"]:
            if not os.path.exists(directory + folder):
                os.makedirs(directory + folder)
        self.mbox = mailbox.Maildir(directory, create=True)

    def select_mailbox(self, dirname):
        directory = "maildir/" + dirname + "/"
        self.mbox = mailbox.Maildir(directory, create=False)
        return self.mbox

    def add_mail(self, message):
        self.mbox.lock()
        self.mbox.add(message)
        self.mbox.flush()

    def count_local_mails(self):
        return self.mbox.__len__()
