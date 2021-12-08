import re
import chardet

from email.parser import HeaderParser
from bs4 import BeautifulSoup


class MailParser(object):
    def __init__(self):
        pass

    def get_urls(self, data):
        urls = set(
            re.findall(
                "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                data,
            )
        )
        return list(urls)

    def decode_body(self, body):
        result = chardet.detect(body)
        if not type(body) == unicode:
            if not result["encoding"]:
                result["encoding"] = "ascii"
            body = unicode(body, result["encoding"], "ignore")
        return body

    def get_headers(self, message):
        """https://docs.python.org/2/library/email.message.html#email.message.Message.items"""
        headers = message.items()
        return dict(headers)

    def show_headers(self, header_str):
        parser = HeaderParser()
        headers = parser.parsestr(header_str).items()
        return headers

    def get_subject(self, header_str):
        subject = header_str["Subject"]
        return subject

    def get_sender(self, header_str):
        sender = header_str["From"]
        return sender

    def get_plaintext_body(self, message):
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True)
                dec_body = self.decode_body(body)
                return dec_body
            elif content_type == "text/html":
                html = part.get_payload(decode=True)
                soup = BeautifulSoup(html)
                text = soup.get_text()
                return text
            else:
                return None

    def get_body(self, message):
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type in ["text/plain", "text/html"]:
                body = part.get_payload(decode=True)
                dec_body = self.decode_body(body)
                return dec_body
