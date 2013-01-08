import json

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Sequence

from configobj import ConfigObj


config = ConfigObj("spamcan.cfg")

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, Sequence('account_id_seq'), primary_key=True)
    user_name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))
    protocol = Column(String(255))
    hostname = Column(String(255))
    smtp_host = Column(String(255))

    def __init__(self, account_config):
        self.user_name = account_config["user_name"]
        self.password = account_config["password"]
        self.protocol = account_config["protocol"]
        self.hostname = account_config["hostname"]
        self.smtp_host = account_config["smtp_host"]

    def __repr__(self):
        return "<User('%s','%s')>" % (self.user_name,
                                            self.hostname,)


class Database(object):
    def __init__(self):
        db_engine = create_engine(config['database'], poolclass=NullPool)
        db_engine.echo = False

        Base.metadata.create_all(db_engine)
        self.Session = sessionmaker(bind=db_engine)

    def add_account(self, account_config):
        session = self.Session()
        account = Account(account_config)
        session.add(account)
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()

    def fetch(self):
        session = self.Session()
        try:
            row = session.query(Account)
        except SQLAlchemyError:
            return None
        return row


if __name__ == "__main__":
    db = Database()
    with open("accounts.json", "rb") as account_file:
        for line in account_file:
            if line.startswith("#"):
                continue
            account_config = json.loads(line)
            db.add_account(account_config)
    for account in db.fetch():
        print repr(account)
