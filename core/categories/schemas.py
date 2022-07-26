import uuid
from decimal import Decimal

from pydantic import BaseModel

from core.categories.models import CategoryType


class CategoryBase(BaseModel):
    name: str
    type: CategoryType
    starting_balance: Decimal


class CategoryCreate(CategoryBase):
    pass


class CategoryGet(CategoryBase):
    id: int
    user_id: uuid.UUID
