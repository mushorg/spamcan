from modules.protocols import imap_util, pop_util


class MailUtil(object):

    def __init__(self):
        self.imap_handler = imap_util.IMAPUtil()
        self.pop_handler = pop_util.POPUtil()

    def request(self, account):
        protocol_handler = None
        if account.protocol == "imap":
            self.imap_handler.imap_connect(account.user_name,
                                      account.password,
                                      account.hostname)
            protocol_handler = self.imap_handler
        elif account.protocol == "pop3":
            self.pop_handler.pop_connect(account.user_name,
                                    account.password,
                                    account.hostname)
            protocol_handler = self.pop_handler
        return protocol_handler
