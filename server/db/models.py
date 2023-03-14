from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from db.database import Base


class DbOrder(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    creation_time = Column(DateTime)
    change_time = Column(DateTime)
    status = Column(String)
    side = Column(String)
    price = Column(DECIMAL)
    amount = Column(Integer)
    instrument = Column(String)
    uuid = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("DbUser", back_populates="orders")


class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    username = Column(String, unique=True)

    orders = relationship("DbOrder", back_populates="user")
