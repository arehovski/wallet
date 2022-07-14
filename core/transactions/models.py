import datetime
import enum
import uuid
from decimal import Decimal

from sqlalchemy import Column, Numeric, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings.db import Base


class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class Transaction(Base):
    __tablename__ = "transaction"

    id: uuid.UUID = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    category_from_id = Column(Integer, ForeignKey("category.id"), nullable=False, index=True)
    category_to_id = Column(Integer, ForeignKey("category.id"), nullable=False, index=True)
    amount: Decimal = Column("amount", Numeric(16, 2), nullable=False)
    type: enum.Enum = Column("type", Enum(TransactionType), nullable=False, index=True)
    created: datetime.datetime = Column("created", DateTime, default=datetime.datetime.now, nullable=False, index=True)

    user = relationship("User", back_populates="transactions")
    category_from = relationship("Category", back_populates="transactions_from")
    category_to = relationship("Category", back_populates="transactions_to")
