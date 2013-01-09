import poplib


def get_mails(user_name, password, hostname):
    M = poplib.POP3(hostname)
    M.set_debuglevel(0)
    M.user(user_name)
    M.pass_(password)

    print M.getwelcome()
    print "Mails in inbox:", M.stat()
