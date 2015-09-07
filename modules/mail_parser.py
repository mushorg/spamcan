import re
import hashlib
import chardet

from email.parser import HeaderParser
from BeautifulSoup import BeautifulSoup, SoupStrainer


class MailParser(object):

    def __init__(self):
        pass

    def get_urls(self, data):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
        return set(urls)

    def decode_body(self, body):
        result = chardet.detect(body)
        if not type(body) == unicode:
            if not result['encoding']:
                result['encoding'] = "ascii"
            body = unicode(body, result['encoding'], "ignore")
        return body


#https://docs.python.org/2/library/email.message.html#email.message.Message.items
    def get_headers(self,message):
	headers = message.items()
	return "\n".join("%s: %s" % tup for tup in headers)


    def get_body(self,message):
        for part in message.walk():
            if part.get_content_type() in ["text/plain", "text/html"]:
		        body = part.get_payload(decode=True)
		        dec_body = self.decode_body(body)
		        return dec_body
	        else :
		        return

    def process_html(self, body):
        return

    def process_attachment(self,part):
        return

    def walk(self, message):
        url_list = []
        for part in message.walk():
            if part.get_content_type():
                if part.get_content_type() in ["text/plain", "text/html"]:
                    body = part.get_payload(decode=True)
                    dec_body = self.decode_body(body)
                    url_list.extend(self.get_urls(dec_body))
                elif part.get_content_type() == "image/jpeg":
                    image = part.get_payload(decode=True)
                    name = hashlib.md5(image).hexdigest()
                    with open("data/files/" + name, "wb") as img_file:
                        img_file.write(image)
        return url_list
