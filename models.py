from sqlalchemy import Column, Integer, String, Float
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

    price_per_unit = Column(Float, default=0.0) # Цена за 1 шт.
    manufacturer_url = Column(String, nullable=True) # Ссылка на производителя