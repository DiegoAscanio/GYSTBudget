import pytest

from models.budget import *
from db import create_db_and_tables

# BEGIN BUDGET TESTS

def test_create_db():
    create_db_and_tables()

def test_crud_create_budget() -> None :
    from sqlmodel import select
    from models.budget import Budget, BudgetCreate
    from crud.budget import create_budget
    from db import get_session
    
    session = next(get_session())
    budget = BudgetCreate(title = 'Budget Teste')
    create_budget(budget)
    budget_db = session.exec(select(Budget).where(Budget.title == 'Budget Teste')).first()
    assert budget_db

def test_crud_retrieve_budget() -> None:
    from crud.budget import retrieve_budget
    budget = retrieve_budget(1)
    assert budget

def test_crud_retrieve_budgets() -> None:
    from crud.budget import retrieve_budgets
    budgets = retrieve_budgets()
    assert budgets

def test_crud_update_budget():
    from models.budget import BudgetUpdate
    from crud.budget import update_budget
    budget_update = BudgetUpdate(title = 'New Budget')
    db_budget = update_budget(1, budget_update)
    assert db_budget.title == 'New Budget' and db_budget.id == 1

def test_crud_delete_budget():
    from models.budget import BudgetCreate
    from crud.budget import create_budget, delete_budget, retrieve_budget
    budget = BudgetCreate(title = 'Budget a ser deletado')
    budget = create_budget(budget)
    budget_id = budget.id
    delete_budget(budget_id)
    with pytest.raises(Exception):
        retrieve_budget(budget_id)

# END BUDGET TESTS
