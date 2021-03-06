import os

from sqlalchemy import Boolean, Sequence
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


database_url = os.getenv("DATABASE_URL", "postgresql://postgres:POSTGRES@localhost:5432/tgbot_base")
engine = create_engine(database_url)

Session_db = sessionmaker(bind=engine)
Base = declarative_base()   # : DeclarativeMeta


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    is_bot = Column(Boolean, nullable=False, default=False)
    last_name = Column(String)
    username = Column(String)
    messages = relationship("MessageModel", back_populates="author")


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)  # Sequence("messages_table_seq", start=1, increment=1, optional=True),
    author_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    author = relationship("UserModel", back_populates="messages")
