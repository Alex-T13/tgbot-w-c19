# from pydantic.decorator import wraps
from functools import wraps
from typing import Callable
from contextlib import closing

from db.database import Session_db, UserModel, MessageModel
from telegram.types import Message


def using_session_db(func: Callable):
    @wraps(func)
    def _wrapped(*args, **kwargs):
        with closing(Session_db()) as session:
            return func(session, *args, **kwargs)

    return _wrapped


@using_session_db
def create_user(session: Session_db, data: Message) -> UserModel:
    user = UserModel(           # **data.from_.dict())
        id=data.from_.id,
        first_name=data.from_.first_name,
        is_bot=data.from_.is_bot,
        last_name=data.from_.last_name,
        username=data.from_.username,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@using_session_db
def get_all_users(session: Session_db, skip: int = 0, limit: int = 100):
    return session.query(UserModel).offset(skip).limit(limit).all()


@using_session_db
def get_single_user(session: Session_db, user_id):
    return session.query(UserModel).filter(UserModel.id == user_id).first()


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


@using_session_db
def get_all_messages(session: Session_db, skip: int = 0, limit: int = 100):
    return session.query(MessageModel).offset(skip).limit(limit).all()
