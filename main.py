from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from core.categories.api import router as categories_router
from core.users.api import fastapi_users
from core.users.schemas import UserRead, UserCreate, UserUpdate
from settings.auth import auth_backend

app = FastAPI()


def wallet_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Wallet app",
        version="0.1.0",
        description="Personal wallet app OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = wallet_openapi

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

app.include_router(categories_router, prefix="categories", tags=["categories"])
