import uuid

from fastapi import Depends
from fastapi_users import UUIDIDMixin, BaseUserManager

from core.users.models import User, get_user_db
from settings.common import TOKEN_SECRET


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = TOKEN_SECRET
    verification_token_secret = TOKEN_SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
