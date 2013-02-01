## Based on http://code.activestate.com/recipes/534131/

import SocketServer


class Message(object):
    def __init__(self):
        self.data = "fooo"
        self.size = len(self.data)
        self.top = "foo"
        self.bot = "bar"


def handleUser(data, msg):
    return "+OK user accepted"


def handlePass(data, msg):
    return "+OK pass accepted"


def handleStat(data, msg):
    return "+OK 1 %i" % msg.size


def handleList(data, msg):
    return "+OK 1 messages (%i octets)\r\n1 %i\r\n." % (msg.size, msg.size)


def handleTop(data, msg):
    cmd, num, lines = data.split()
    assert num == "1", "unknown message number: %s" % num
    lines = int(lines)
    text = msg.top + "\r\n\r\n" + "\r\n".join(msg.bot[:lines])
    return "+OK top of message follows\r\n%s\r\n." % text


def handleRetr(data, msg):
    return "+OK %i octets\r\n%s\r\n." % (msg.size, msg.data)


def handleDele(data, msg):
    return "+OK message 1 deleted"


def handleNoop(data, msg):
    return "+OK"


def handleQuit(data, msg):
    return "+OK POP3 server signing off"

dispatch = dict(
    USER=handleUser,
    PASS=handlePass,
    STAT=handleStat,
    LIST=handleList,
    TOP=handleTop,
    RETR=handleRetr,
    DELE=handleDele,
    NOOP=handleNoop,
    QUIT=handleQuit,
)


class TCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.request.sendall("+OK SpamCan test server ready\r\n")
        while True:
            self.data = self.request.recv(1024).strip()
            print repr(self.data)
            if self.data:
                command = self.data.split(" ", 1)[0]
                cmd = dispatch[command]
                self.request.sendall(cmd(self.data, Message()) + "\r\n")
                if command == "QUIT":
                    break
            else:
                break


def pop_server(port):
    return SocketServer.TCPServer(("localhost", port), TCPHandler)

if __name__ == "__main__":
    server = pop_server(8088)
    server.serve_forever()
