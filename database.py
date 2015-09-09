import json
import os

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Text

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, Sequence('account_id_seq'), primary_key=True)
    user_name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))
    protocol = Column(String(255))
    hostname = Column(String(255))
    smtp_host = Column(String(255))
    remote_count = Column(Integer)
    mailbox_count = Column(Integer)
    urls_count = Column(Integer)

    def __init__(self, account_config):
        self.user_name = account_config["user_name"]
        self.password = account_config["password"]
        self.protocol = account_config["protocol"]
        self.hostname = account_config["hostname"]
        self.smtp_host = account_config["smtp_host"]
        self.remote_count = 0
        self.mailbox_count = 0
        self.urls_count = 0

    def __repr__(self):
        return "<User('%s','%s')>" % (self.user_name,
                                      self.hostname,)

class Mail(Base):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    headers = Column(Text)
    subject = Column(Text)
    sender = Column(Text)
    body = Column(Text)

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    mail_id = Column(Integer, ForeignKey('mail.id'))
    mime = Column(String(255))
    file = Column(String(255))

class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    mail_id = Column(Integer, ForeignKey('mail.id'))
    url = Column(String(255))

class Database(object):
    def __init__(self, conf_dir="conf"):
        try:
            with open(os.path.join(conf_dir, "spamcan.json"), "rb") as config_file:
                init_config = json.loads(config_file.read())
        except IOError:
            raise IOError("Modify and rename conf/spamcan.json.dist to conf/spamcan.json")

        self.db_path = init_config["database"]
        db_engine = create_engine(self.db_path, poolclass=NullPool)
        db_engine.echo = False

        Base.metadata.create_all(db_engine)
        self.Session = sessionmaker(bind=db_engine)
        self.session = self.Session()
        try:
            with open(os.path.join(conf_dir, "accounts.json"), "rb") as account_file:
                for line in account_file:
                    if line.startswith("#"):
                        continue
                    account_config = json.loads(line)
                    self.add_account(account_config)
        except IOError:
            raise IOError("Modify and rename conf/accounts.json.dist to conf/accounts.json")

    def add_account(self, account_config):
        account = Account(account_config)
        self.session.add(account)
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()

    def fetch_all(self):
        try:
            row = self.session.query(Account)
        except SQLAlchemyError:
            return None
        return row

    # mail methods
    def fetch_mails(self):
        try:
            row = self.session.query(Mail)
        except SQLAlchemyError:
            return None
        return row

    def fetch_mail_by_id(self, mail_id):
        try:
            row = self.session.query(Mail).filter(
                                    Mail.id == mail_id).first()
        except SQLAlchemyError:
            return None
        return row

    def fetch_mail_by_user(self, acc_id):
        try:
            row = self.session.query(Mail).filter(
                                    Mail.account_id == acc_id)
        except SQLAlchemyError:
            return None
        return row

    # url methods
    def fetch_urls(self):
        try:
            row = self.session.query(Url)
        except SQLAlchemyError:
            return None
        return row

    def fetch_by_id(self, account_id):
        try:
            row = self.session.query(Account).filter(
                                    Account.account_id == account_id).all()
        except SQLAlchemyError:
            return None
        return row[0]

    def delete_by_id(self, account_id):
        account = self.fetch_by_id(account_id)
        self.session.delete(account)
        self.session.commit()

    def fetch_by_id_list(self, account_id_list):
        accounts = []
        for account_id in account_id_list:
            accounts.append(self.fetch_by_id(account_id))
        return accounts

    def update_account(self, account):
        self.session.flush()
        self.session.commit()
