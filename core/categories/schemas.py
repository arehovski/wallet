from decimal import Decimal

from pydantic import BaseModel

from core.categories.models import CategoryType


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
    starting_balance: Decimal


