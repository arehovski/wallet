import uuid

from fastapi_users import FastAPIUsers

from core.managers.users import get_user_manager
from core.models.users import User
from settings.auth import auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
