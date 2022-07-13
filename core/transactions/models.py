import datetime
import uuid
from decimal import Decimal

from sqlalchemy import Column, Numeric, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from settings.db import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id: uuid.UUID = Column("id", PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("user.id"))
    category_from_id = Column(Integer, ForeignKey("category.id"))
    category_to_id = Column(Integer, ForeignKey("category.id"))
    amount: Decimal = Column("amount", Numeric(16, 2), nullable=False)
    created: datetime.datetime = Column("created", DateTime, default=datetime.datetime.now) # TODO add index and ordering

    user = relationship("User", back_populates="transactions")
    category_from = relationship("Category", back_populates="transactions_from")
    category_to = relationship("Category", back_populates="transactions_to")

