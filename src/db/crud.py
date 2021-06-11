from functools import wraps
from typing import Callable, List
from contextlib import closing

from custom_logging import logger
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
        lang="en",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@using_session_db
def get_user_by_id(session: Session_db, user_id: int) -> UserModel:
    user = session.query(UserModel).get(user_id)   # filter(UserModel.id == user_id).first()
    logger.debug(f"get single user: {user}")
    return user


@using_session_db
def get_all_users(session: Session_db, ) -> List[UserModel]:
    users = session.query(UserModel).all()
    return users


# @using_session_db
# def get_all_users(session: Session_db, skip: int = 0, limit: int = 100):
#     return session.query(UserModel).offset(skip).limit(limit).all()


@using_session_db
def save_message(session: Session_db, data: Message) -> MessageModel:
    message = MessageModel(
        # id=data.message_id,
        author_id=data.from_.id,
        text=data.text,
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    # logger.debug(f"save message: {message}")

    return message


@using_session_db
def get_last_message(session: Session_db, user_id: int) -> MessageModel:
    l_message = session.query(MessageModel).filter(
        MessageModel.author_id == user_id).order_by(MessageModel.created_at.desc()).first()

    return l_message
