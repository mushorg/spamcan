import imaplib
import email


def get_mails(user_name, password, hostname):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('myusername@gmail.com', 'mypassword')
    mail.list()
    mail.select("inbox")

    result, data = mail.uid('search', None, "ALL")
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_string(raw_email)

    print email_message['To']
    print email.utils.parseaddr(email_message['From'])
    print email_message.items()
