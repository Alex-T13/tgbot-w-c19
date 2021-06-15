import os
# import re

from sqlalchemy import Boolean  # Sequence
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


database_url = os.getenv("DATABASE_URL", "postgres://postgres:POSTGRES@localhost:5432/tgbot_base")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
engine = create_engine(database_url)

Session_db = sessionmaker(bind=engine)
Base = declarative_base()   # : DeclarativeMeta


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    is_bot = Column(Boolean, nullable=False, server_default='false')
    last_name = Column(String)
    username = Column(String)
    lang = Column(String, nullable=False, server_default="ru")
    messages = relationship("MessageModel", back_populates="author", cascade="all, delete", passive_deletes=True)


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)  # Sequence("messages_table_seq", start=1, increment=1, optional=True),
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    text = Column(Text)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    author = relationship("UserModel", back_populates="messages")
