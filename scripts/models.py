"""SQLModel table for supermarket sales (SuperMarket Analysis sheet)."""

from datetime import datetime, time
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel

from config import get_table_name


class SupermarketSale(SQLModel, table=True):
    __tablename__ = get_table_name()

    invoice_id: str = Field(primary_key=True, max_length=32)
    branch: Optional[str] = Field(default=None, max_length=50, index=True)
    city: Optional[str] = Field(default=None, max_length=50, index=True)
    customer_type: Optional[str] = Field(default=None, max_length=50)
    gender: Optional[str] = Field(default=None, max_length=20)
    product_line: Optional[str] = Field(default=None, max_length=100, index=True)
    unit_price: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=4)
    quantity: Optional[int] = None
    tax_5: Optional[Decimal] = Field(default=None, max_digits=14, decimal_places=4)
    sales: Optional[Decimal] = Field(default=None, max_digits=14, decimal_places=4)
    sale_date: Optional[datetime] = Field(default=None, index=True)
    sale_time: Optional[time] = None
    payment: Optional[str] = Field(default=None, max_length=50)
    cogs: Optional[Decimal] = Field(default=None, max_digits=14, decimal_places=4)
    gross_margin_percentage: Optional[Decimal] = Field(default=None, max_digits=14, decimal_places=6)
    gross_income: Optional[Decimal] = Field(default=None, max_digits=14, decimal_places=4)
    rating: Optional[Decimal] = Field(default=None, max_digits=4, decimal_places=2)
