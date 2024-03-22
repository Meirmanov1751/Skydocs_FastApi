from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.dialects.postgresql import OID, BYTEA
from src.brd.test.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    price = Column(Float)
    tax = Column(Float, nullable=True)


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(BigInteger, index=True)
    data = Column(BYTEA)
