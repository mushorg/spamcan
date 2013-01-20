import mailbox


class MaildirUtil(object):

    def __init__(self):
        pass

    def creat_mailbox(self, dirname):
        self.mbox = mailbox.Maildir(dirname)

    def add_mail(self, message):
        self.mbox.add(message)
