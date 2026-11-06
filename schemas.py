from pydantic import BaseModel, HttpUrl, model_validator, Field
from typing import Optional
from datetime import datetime

#----Tool----
class ToolBase(BaseModel):
    Type: str
    Name: str
    D: str
    S: Optional[str] = None
    L: Optional[str] = None
    I: Optional[str] = None  # noqa: E741
    Z: Optional[str] = None
    Kol: int
    price_per_unit: float = 0.0
    manufacturer_url: Optional[HttpUrl] = None

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    Type: Optional[str] = None
    Name: Optional[str] = None
    D: Optional[str] = None
    S: Optional[str] = None
    L: Optional[str] = None
    I: Optional[str] = None  # noqa: E741
    Z: Optional[str] = None
    Kol: Optional[int] = None
    price_per_unit: Optional[float] = None
    manufacturer_url: Optional[HttpUrl] = None

class Tool(ToolBase):
    id: int
    total_cost: Optional[float] = None # Поле для общей стоимости

    @model_validator(mode='after')
    def calculate_total_cost(self):
        # self.Kol и self.price_per_unit здесь уже гарантированно являются int и float
        self.total_cost = self.Kol * (self.price_per_unit or 0.0)
        return self

    class Config:
        from_attributes = True


#---User---
class User(BaseModel):
    name: str
    surname: str

    class Config:
        from_attributes = True

class UserCreat(User):
    name: str = Field(..., alias='Name')
    surname: str = Field(..., alias='Surname')

    class Config:
        populate_by_name = True

class ReadUser(User):
    id: int

#---Issue---
class IssueCreate(BaseModel):
    user_id: int
    tool_id: int
    quantity: int

class HistoryTool(BaseModel):
    id: int
    user_id: int
    tool_id: int
    quantity: int
    issue_date: datetime

    class Config:
        from_attributes = True

class HistoryItem(BaseModel):
    id: int
    issue_date: datetime
    user_fio: str
    tool_name: str
    quantity: int
