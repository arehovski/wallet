from dotenv import load_dotenv
from fastapi_users.authentication import BearerTransport, AuthenticationBackend, JWTStrategy

from settings.common import AUTH_SECRET

load_dotenv()

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=AUTH_SECRET, lifetime_seconds=None)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
