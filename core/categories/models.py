import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings.db import Base


class CategoryType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ACCOUNT = "account"


class Category(Base):
    __tablename__ = "category"

    id: int = Column("id", Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    name: str = Column("name", String, unique=True)
    type: enum.Enum = Column("type", Enum(CategoryType))

    user = relationship("User", back_populates="categories")
    transactions_from = relationship("Transaction", back_populates="category_from")
    transactions_to = relationship("Transaction", back_populates="category_to")
