from typing import List, Text, Union, Dict
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class JsonApiSchema(BaseModel):
    errors: Optional[List[Text]] = None
    data: Union[List, Optional[Dict]] = None


class Chat(BaseModel):
    first_name: Optional[str] = Field(default=None)
    id: int = Field(...)
    last_name: Optional[str] = Field(default=None)
    type: str = Field(...)
    username: Optional[str] = Field(default=None)


class User(BaseModel):
    first_name: str = Field(...)
    id: int = Field(...)
    is_bot: bool = Field(...)
    last_name: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)

    class Config:
        orm_mode = True


UserList = List[User]


class UserListApiSchema(JsonApiSchema):
    data: UserList


class MessageEntity(BaseModel):
    language: Optional[str] = Field(default=None)
    length: int = Field(...)
    offset: int = Field(...)
    type: str = Field(...)
    url: Optional[str] = Field(default=None)
    user: Optional[User] = Field(default=None)


class Voice(BaseModel):
    file_id: str = Field(...)
    file_unique_id: str = Field(...)
    duration: int = Field(...)
    mime_type: Optional[str] = Field(default=None)
    file_size: Optional[int] = Field(default=None)


class PhotoSize(BaseModel):
    file_id: str = Field(...)
    file_unique_id: str = Field(...)
    width: int = Field(...)
    height: int = Field(...)
    file_size: Optional[int] = Field(default=None)


class MaskPosition(BaseModel):
    point: str = Field(...)
    x_shift: float = Field(...)
    y_shift: float = Field(...)
    scale: float = Field(...)


class Sticker(BaseModel):
    file_id: str = Field(...)
    file_unique_id: str = Field(...)
    width: int = Field(...)
    height: int = Field(...)
    is_animated: bool = Field(...)
    thumb: Optional[PhotoSize] = Field(default=None)
    emoji: Optional[str] = Field(default=None)
    set_name: Optional[str] = Field(default=None)
    mask_position: Optional[MaskPosition] = Field(default=None)
    file_size: Optional[int] = Field(default=None)


class Animation(BaseModel):
    file_id: str = Field(...)
    file_unique_id: str = Field(...)
    width: int = Field(...)
    height: int = Field(...)
    duration: int = Field(...)
    thumb: Optional[PhotoSize] = Field(default=None)
    file_name: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None)
    file_size: Optional[int] = Field(default=None)


class Document(BaseModel):
    file_id: str = Field(...)
    file_unique_id: str = Field(...)
    thumb: Optional[PhotoSize] = Field(default=None)
    file_name: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None)
    file_size: Optional[int] = Field(default=None)


class ReplyToMessageId(BaseModel):
    message_id: int = Field(...)
    from_: Optional[User] = Field(default=None)
    date: int = Field(...)
    chat: Chat = Field(...)
    text: Optional[str] = Field(default=None)
    entities: List[MessageEntity] = Field(default_factory=list)
    animation: Optional[Animation] = Field(default=None)
    document: Optional[Document] = Field(default=None)
    sticker: Optional[Sticker] = Field(default=None)
    voice: Optional[Voice] = Field(default=None)

    class Config:
        fields = {
            "from_": "from",
        }


class Message(ReplyToMessageId):
    reply_to_message: Optional[ReplyToMessageId] = Field(default=None)

    class Config:
        orm_mode = True


class EditedMessage(Message):
    edit_date: int = Field(...)


class Update(BaseModel):
    message: Optional[Message] = Field(default=None)
    edited_message: Optional[EditedMessage] = Field(default=None)
    update_id: int = Field(...)


class WebhookInfo(BaseModel):
    allowed_updates: List[str] = Field(default_factory=list)
    has_custom_certificate: bool = Field(...)
    ip_address: Optional[str] = Field(default=None)
    last_error_date: Optional[int] = Field(default=None)
    last_error_message: Optional[str] = Field(default=None)
    max_connections: Optional[int] = Field(default=None)
    pending_update_count: int = Field(...)
    url: str = Field(...)


# ==== post setup =========================================

Message.update_forward_refs()
