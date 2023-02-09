from typing import List, Optional
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from pydantic import condecimal
from datetime import datetime
from enum import IntEnum

# CATEGORY BEGIN #

class CategoryBase(SQLModel):
    name: str=Field(index=True)

class Category(CategoryBase, table=True):
    transactions: Optional[List['Transaction']]=Relationship(
        back_populates='category',
    )
    budget_links: Optional[List['CategoryBudgetLink']] = Relationship(
        back_populates='category' 
    )
    id : Optional[int]=Field(default=None, primary_key=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id : int

class CategoryUpdate(SQLModel):
    name: Optional[str] = None

# CATEGORY END #

# BUDGET BEGIN #

class BudgetBase(SQLModel):
    title: str
    date : datetime=Field(default_factory=datetime.now, index=True)

class Budget(BudgetBase, table=True):
    category_links : Optional[List['CategoryBudgetLink']] = Relationship(
        back_populates='budget' 
    )
    id : Optional[int]=Field(default=None, primary_key=True)
    @property
    def total(self) -> condecimal(max_digits=12, decimal_places=2) :
        amounts = [link.amount for link in self.category_links]
        return sum(amounts)
 
class BudgetCreate(BudgetBase):
    pass

class BudgetRead(BudgetBase):
    id : int

class BudgetUpdate(SQLModel):
    title: Optional[str] = None
    date: Optional[datetime] = None

# BUDGET END #

# TRANSACTION BEGIN #

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

# TRANSACTION END #

# ORIGIN BEGIN #

class OriginBase(SQLModel):
    name: str=Field(index=True)

class Origin(OriginBase, table=True):
    transactions: Optional[List['Transaction']]=Relationship(
        back_populates='origin',
    )
    id : Optional[int]=Field(default=None, primary_key=True)

class OriginCreate(OriginBase):
    pass

class OriginRead(OriginBase):
    id : int

class OriginUpdate(SQLModel):
    name: Optional[str] = None

# ORIGIN END #

# LINK BEGIN #

class CategoryBudgetLinkBase(SQLModel):
    amount: condecimal(max_digits=12, decimal_places=2)  = Field(default = 0)

class CategoryBudgetLink(CategoryBudgetLinkBase, table = True):
    category_id: Optional[int] = Field(
        default = None, foreign_key='category.id', primary_key=True
    )
    budget_id: Optional[int] = Field(
        default = None, foreign_key='budget.id', primary_key=True
    )
    category: 'Category' = Relationship(
        back_populates='budget_links'
    )
    budget: 'Budget' = Relationship(
        back_populates='category_links'
    )

class CategoryBudgetLinkCreate(CategoryBudgetLinkBase):
    pass

class CategoryBudgetLinkRead(CategoryBudgetLinkBase):
    category_id: int
    budget_id: int

class CategoryBudgetLinkReadWithCategories(CategoryBudgetLinkRead):
    categories : List['CategoryRead'] = []

class CategoryBudgetLinkReadWithBudgets(CategoryBudgetLinkRead):
    budgets : List['BudgetRead'] = []

class CategoryBudgetLinkUpdate(SQLModel):
    amount: Optional[Decimal] = None

# LINK END #

