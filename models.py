from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref
from database import Base

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

    price_per_unit = Column(Float, default=0.0)
    manufacturer_url = Column(String, nullable=True)

    # Используем backref со строковым именем класса
    history = relationship("HistoryTool", backref=backref("tool", lazy="select"))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)

    history = relationship("HistoryTool", backref=backref("user", lazy="select"))

class HistoryTool(Base):
    __tablename__ = 'history_tools'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tool_id = Column(Integer, ForeignKey('tools.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
