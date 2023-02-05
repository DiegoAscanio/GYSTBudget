from models.budget import *
from sqlmodel import Session, select
from db import get_session

def create_budget(budget: BudgetCreate, session: Session = next(get_session())):
    db_budget = Budget.from_orm(budget)
    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    return db_budget

def retrieve_budget(budget_id : int, session: Session = next(get_session())):
    budget = session.get(Budget, budget_id)
    if not budget:
        raise Exception('Budget not found')
    return budget

def retrieve_budgets(session: Session = next(get_session()), offset: int = 0, limit: int = 100):
    budgets = session.exec(select(Budget).offset(offset).limit(limit)).all()
    return budgets

def update_budget(budget_id : int, budget: BudgetUpdate, session: Session = next(get_session())):
    db_budget = session.get(Budget, budget_id)
    if not db_budget:
        raise Exception('Budget not found')
    budget_data = budget.dict(exclude_unset=True)
    for key, value in budget_data.items():
        setattr(db_budget, key, value)
    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    return db_budget

def delete_budget(budget_id: int, session: Session = next(get_session())):
    budget = session.get(Budget, budget_id)
    if not budget:
        raise Exception('Budget not found')
    session.delete(budget)
    session.commit()
    return {'ok': True}

