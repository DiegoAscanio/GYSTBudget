from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from models.categorybudgetlink import CategoryBudgetLink
    from models.transaction import Transaction

class CategoryBase(SQLModel):
    name: str=Field(index=True)

class Category(CategoryBase, table=True):
    __table_args__ = (UniqueConstraint('name'),)
    transactions: Optional[List['Transaction']]=Relationship(
        back_populates='category',
    )
    budget_links: Optional[List['CategoryBudgetLink']] = Relationship(
        back_populates='category',
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan'
        }
    )
    id : Optional[int]=Field(default=None, primary_key=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id : int

class CategoryUpdate(SQLModel):
    name: Optional[str] = None

