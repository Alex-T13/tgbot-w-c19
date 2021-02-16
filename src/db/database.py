import os
from contextlib import closing
from functools import wraps
from typing import Callable

from delorean import now
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from telegram.types import Message
import config


database_url = os.getenv("DATABASE_URL", config.settings.database_url)
engine = create_engine(database_url)

Session_db = sessionmaker(bind=engine)
Model_db = declarative_base()


def using_session_db(func: Callable):
    @wraps(func)
    def _wrapped(*args, **kwargs):
        with closing(Session_db()) as session:
            return func(session, *args, **kwargs)

    return _wrapped


class UserModel(Model_db):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    is_bot = Column(Boolean, nullable=False, default=False)
    last_name = Column(Text)
    username = Column(Text)


class MessageModel(Model_db):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime, nullable=False, default=lambda: now().datetime)


@using_session_db
def create_user(session: Session_db, data: Message) -> UserModel:
    user = UserModel(**data.from_.dict())
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_all_users(session: Session_db, skip: int = 0, limit: int = 100):
    return session.query(UserModel).offset(skip).limit(limit).all()


@using_session_db
def save_message(session: Session_db, data: Message) -> MessageModel:
    message = MessageModel(
        id=data.message_id,
        author_id=data.from_.id,
        text=data.text,
    )
    session.add(message)
    session.commit()
    session.refresh(message)

    return message


def get_all_messages(session: Session_db, skip: int = 0, limit: int = 100):
    return session.query(MessageModel).offset(skip).limit(limit).all()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


        # class Parent(Base):
        #     __tablename__ = 'parent'
        #     id = Column(Integer, primary_key=True)
        #     children = relationship("Child")
        #
        # class Child(Base):
        #     __tablename__ = 'child'
        #     id = Column(Integer, primary_key=True)
        #     parent_id = Column(Integer, ForeignKey('parent.id'))

