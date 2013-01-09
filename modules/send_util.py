import smtplib

from email.mime.text import MIMEText
from email.Utils import formatdate


def reply(to, subj, body, user_name, smtp_host):
    msg = MIMEText("Hello, how can I help you?" + "\n\n" + body.encode("UTF-8"))
    msg["From"] = user_name
    msg["To"] = to
    msg["Subject"] = "Re: " + subj
    msg['Date'] = formatdate(localtime=True)
    server = smtplib.SMTP(smtp_host)
    try:
        server.sendmail(msg["From"], msg["To"], msg.as_string())
    except:
        print "Error sending mail"
    server.quit()
    print "Send message to", to
