import uuid
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, validator

from core.categories.models import CategoryType


class CategoryBase(BaseModel):
    name: str
    starting_balance: Decimal

    @validator("starting_balance")
    def is_positive(cls, value: Decimal):
        if value < Decimal(0):
            raise ValueError("Must be greater than 0")
        return value


class CategoryCreate(CategoryBase):
    type: CategoryType


class CategoryUpdate(CategoryBase):
    __annotations__ = {k: Optional[v] for k, v in CategoryBase.__annotations__.items()}


class CategorySchema(CategoryBase):
    id: int
    type: CategoryType
    user_id: uuid.UUID

    class Config:
        orm_mode = True
