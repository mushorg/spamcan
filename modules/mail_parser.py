import re
import hashlib

import chardet


def get_attachments(message):
    for part in message.walk():
        if part.get_content_type():
            if part.get_content_type() in ["text/plain", "text/html"]:
                body = part.get_payload(decode=True)
            elif part.get_content_type() == "image/jpeg":
                image = part.get_payload(decode=True)
                name = hashlib.md5(image).hexdigest()
                with open("bins/" + name, "wb") as img_file:
                    img_file.write(image)


def decode_body(body):
    result = chardet.detect(body)
    if not type(body) == unicode:
        if not result['encoding']:
            result['encoding'] = "ascii"
        body = unicode(body, result['encoding'], "ignore")


def get_urls(data):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)


def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()
