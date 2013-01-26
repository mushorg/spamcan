import imaplib


class IMAPSUtil(object):
    def __init__(self):
        pass

    def imaps_connect(self, user_name, password, hostname):
        self.mail = imaplib.IMAP4_SSL(hostname)
        self.mail.login(user_name, password)

    def get_stats(self):
    	print self.mail.list()
        data = self.mail.select('Inbox')[1]
        return int(data[0])


if __name__ == "__main__":
    imaps_connection = IMAPSSUtil("user_name", "password", "hostname")
    imaps_connection.get_stats()