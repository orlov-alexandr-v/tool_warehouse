from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base
from database import Base

Base = declarative_base()  # noqa: F811

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    Type = Column(String, index=True)
    Name = Column(String, index=True)
    D = Column(String, index=True)
    S = Column(String)
    L = Column(String)
    I = Column(String) # noqa: E741
    Z = Column(String)
    Kol = Column(Integer)

    price_per_unit = Column(Float, default=0.0) # Цена за 1 шт.
    manufacturer_url = Column(String, nullable=True) # Ссылка на производителя


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
