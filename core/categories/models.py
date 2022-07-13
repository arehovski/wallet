from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from settings.db import Base


class Category(Base):
    __tablename__ = "category"

    id: int = Column("id", Integer, primary_key=True)

    transactions_from = relationship("Transaction", back_populates="category_from")
    transactions_to = relationship("Transaction", back_populates="category_to")
