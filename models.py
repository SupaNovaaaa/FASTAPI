from sqlalchemy import Column,Integer,String,Boolean
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__="posts"

    id = Column(Integer,primary_key=True,nullable=True)
    title = Column(String,nullable=False)
    title = Column(Integer,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE',nullable=False )
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
