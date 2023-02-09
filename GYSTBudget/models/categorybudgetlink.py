from typing import List, Optional, TYPE_CHECKING
from pydantic import condecimal
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.category import Category, CategoryRead
    from models.budget import Budget, BudgetRead

class CategoryBudgetLinkBase(SQLModel):
    amount: condecimal(max_digits=12, decimal_places=2)  = Field(default = 0)

class CategoryBudgetLink(CategoryBudgetLinkBase, table = True):

    category_id: Optional[int] = Field(
        default = None, foreign_key='category.id', primary_key=True, 
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

