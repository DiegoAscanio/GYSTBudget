from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from pydantic import condecimal
from datetime import datetime
from enum import IntEnum

if TYPE_CHECKING:
    from models.category import Category
    from models.origin import Origin


class TransactionTypeEnum(IntEnum):
    expense=1,
    income=2

class TransactionBase(SQLModel):
    type : TransactionTypeEnum
    date : datetime=Field(default_factory=datetime.now, index=True)
    title: str
    amount: condecimal(max_digits=12, decimal_places=2) = Field(default=0)

class Transaction(TransactionBase, table=True):
    id : Optional[int]=Field(default=None, primary_key=True)
    category: Optional['Category'] = Relationship(
        back_populates='transactions',
    )
    origin: Optional['Origin'] = Relationship(
        back_populates='transactions',
    )
    category_id: Optional[int] = Field(default=None, foreign_key='category.id')
    origin_id: Optional[int] = Field(default=None, foreign_key='origin.id')


class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id : int
    category_id : Optional[int]
    origin_id : Optional[int]

class TransactionUpdate(SQLModel):
    type : Optional[IntEnum] = None
    date : Optional[datetime] = None
    title : Optional[str] = None
    amount : Optional[Decimal] = None
    category_id : Optional[int] = None
    origin_id : Optional[int] = None

