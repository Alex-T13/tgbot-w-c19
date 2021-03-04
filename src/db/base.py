# Import all the models, so that Base has them before being
# imported by Alembic
from db.database import Base
from db.database import database_url

from telegram.types import User
from telegram.types import Message
