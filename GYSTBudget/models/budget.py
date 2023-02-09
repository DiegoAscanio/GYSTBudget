from typing import List, Optional, TYPE_CHECKING
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint
from pydantic import condecimal
from datetime import datetime

if TYPE_CHECKING:
    from models.categorybudgetlink import CategoryBudgetLink
    from models.transaction import Transaction

class BudgetBase(SQLModel):
    title: str
    date : datetime=Field(default_factory=datetime.now, index=True)

class Budget(BudgetBase, table=True):
    __table_args__ = (UniqueConstraint('title'),)
    category_links : Optional[List['CategoryBudgetLink']] = Relationship(
        back_populates='budget',
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan'
        }
    )
    transactions : Optional[List['Transaction']] = Relationship(
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
