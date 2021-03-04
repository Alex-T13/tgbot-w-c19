from functools import wraps
from typing import Callable
from contextlib import closing

from db.database import Session_db
from db.database import UserModel
from db.database import MessageModel
from telegram.types import Message


def using_session_db(func_: Callable):
    @wraps(func_)
    def _wrapped(*args, **kwargs):
        with closing(Session_db()) as session:
            return func_(session, *args, **kwargs)

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
def get_single_user(session: Session_db, user_id: int):
    s_user = session.query(UserModel).filter(UserModel.id == user_id).first()
    return s_user


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
def get_last_message(session: Session_db, user_id: int):
    l_message = session.query(MessageModel).filter(
        MessageModel.author_id == user_id).order_by(MessageModel.created_at.desc()).first()

    return l_message
