import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings.db import Base


class CategoryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ACCOUNT = "account"


class Category(Base):
    __tablename__ = "category"

    id: int = Column("id", Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    name: str = Column("name", String, nullable=False)
    type: enum.Enum = Column("type", Enum(CategoryType), nullable=False)
    starting_balance = Column("starting_balance", Numeric(16, 2), default=0)

    user = relationship("User", back_populates="categories")
    transactions_from = relationship("Transaction", back_populates="category_from", foreign_keys="Transaction.category_from_id")
    transactions_to = relationship("Transaction", back_populates="category_to", foreign_keys="Transaction.category_to_id")

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='user_category_uc'),
    )
