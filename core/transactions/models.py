import datetime
import uuid
from decimal import Decimal

from sqlalchemy import Column, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from settings.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: uuid.UUID = Column("id", PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount: Decimal = Column("amount", Numeric(16, 2), nullable=False)
    created: datetime.datetime = Column("created", DateTime, default=datetime.datetime.now)
    modified: datetime.datetime = Column("modified", DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
