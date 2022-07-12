import uuid

from fastapi_users import FastAPIUsers

from core.users.models import User
from core.users.services import get_user_manager
from settings.auth import auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
