"""Pydantic models for Task 3 API."""
from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    """Payload for creating an order (both MySQL and MongoDB)."""
    order_date: date
    product_name: str
    category: str
    region: str
    quantity: int = Field(ge=0)
    sales: float = Field(ge=0)
    profit: float = Field(ge=0)


class OrderUpdate(BaseModel):
    """Payload for updating an order (partial)."""
    order_date: Optional[date] = None
    product_name: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    sales: Optional[float] = Field(None, ge=0)
    profit: Optional[float] = Field(None, ge=0)


class OrderResponse(BaseModel):
    """Order response (unified for both DBs)."""
    id: Union[str, int]
    order_date: date
    product_name: str
    category: str
    region: str
    quantity: int
    sales: float
    profit: float

    class Config:
        from_attributes = True
