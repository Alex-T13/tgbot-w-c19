import os
from contextlib import closing
from functools import wraps
from typing import Callable
from typing import List
from typing import Optional

from delorean import now
# from dynaconf import settings
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

from api.schemas import PostSchema
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
def save_massage(session: Session_db, data: Message) -> Message:
    message = MessageModel(
        id=data.message_id,
        author_id=data.from_.id,
        text=data.text,
    )
    session.add(post)
    session.commit()

    session.refresh(post)

    return post
