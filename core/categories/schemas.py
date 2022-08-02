import uuid
from decimal import Decimal

from pydantic import BaseModel, validator, ValidationError

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
    name: str | None
    starting_balance: Decimal | None


class CategorySchema(CategoryBase):
    id: int
    type: CategoryType
    user_id: uuid.UUID

    class Config:
        orm_mode = True
