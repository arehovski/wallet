import uuid
from decimal import Decimal

from pydantic import BaseModel

from core.categories.models import CategoryType


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
    starting_balance: Decimal


class CategoryGet(BaseModel):
    id: int
    user_id: uuid.UUID
    name: str
    type: CategoryType
    starting_balance: Decimal
