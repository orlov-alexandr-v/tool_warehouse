from pydantic import BaseModel, HttpUrl
from typing import Optional
from database import Base

class ToolBase(BaseModel):
    Type: str
    Name: str
    D: str
    S: Optional[str] = None
    L: Optional[str] = None
    I: Optional[str] = None
    Z: Optional[str] = None
    Kol: int
    price_per_unit: float = 0.0
    manufacturer_url: HttpUrl = None

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    Type: Optional[str] = None
    Name: Optional[str] = None
    D: Optional[str] = None
    S: Optional[str] = None
    L: Optional[str] = None
    I: Optional[str] = None
    Z: Optional[str] = None
    Kol: Optional[int] = None
    price_per_unit: float = None
    manufacturer_url: HttpUrl = None

class Tool(ToolBase):
    id: int
    total_cost: float = None # Поле для общей стоимости

    class Config:
        from_attributes = True