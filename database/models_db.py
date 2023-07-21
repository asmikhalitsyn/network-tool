import os

from sqlalchemy import create_engine, UniqueConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, String, Integer, Column, DateTime
from datetime import datetime

file_path = os.getcwd() + '/check.db'
db_name = 'sqlite:///' + file_path
metadata = MetaData()
Base = declarative_base()


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    host = Column(String, index=True)
    platform = Column(String)
    checkp = relationship('Checkpoint', back_populates='chck')
    hst = relationship('Commands', back_populates='cmd')
    checkpoint_id = Column(Integer, ForeignKey('checkpoint.id'))


class Checkpoint(Base):
    __tablename__ = 'checkpoint'
    id = Column(Integer, primary_key=True)
    checkpoint_name = Column(String, index=True)
    chck = relationship('Host', back_populates='checkp')
    check_to_cmd = relationship('Commands', back_populates='cmd_to_check')
    created_on = Column(DateTime(), default=datetime.now)
    __table_args__ = (UniqueConstraint('checkpoint_name'),
                      )


class Commands(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    command = Column(String, index=True)
    output = Column(String, index=True)
    test_name = Column(String, index=True)
    checkp_id = Column(Integer, ForeignKey('checkpoint.id'))
    host_id = Column(Integer, ForeignKey('host.id'))
    cmd = relationship('Host', back_populates='hst')
    cmd_to_check = relationship('Checkpoint', back_populates='check_to_cmd')


engine = create_engine(db_name)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
session = session_maker()
