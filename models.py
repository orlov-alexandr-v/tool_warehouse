from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
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
    surname = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)


class HistoryTool(Base):
    __tablename__ = 'history_tools'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tool_id = Column(Integer, ForeignKey('tools.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())

    class Config:
        extra = "ignore"