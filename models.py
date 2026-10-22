from sqlalchemy import Column, Integer, String
from database import Base

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    Type = Column(String, index=True)
    Name = Column(String, index=True)
    D = Column(String, index=True)
    S = Column(String)
    L = Column(String)
    I = Column(String)
    Z = Column(String)
    Kol = Column(Integer)