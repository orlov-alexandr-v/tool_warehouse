from pydantic import BaseModel
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

class Tool(ToolBase):
    id: int

    class Config:
        from_attributes = True