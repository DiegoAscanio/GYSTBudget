from models.categorybudgetlink import *
from models.budget import Budget
from models.category import Category
from sqlmodel import Session, select
from db import get_session
import pdb

def create_cb_link(cb_link, category_id: int, budget_id : int , session: Session = next(get_session())):
    db_category = session.get(Category, category_id)
    db_budget= session.get(Budget, budget_id)
    db_cbl = CategoryBudgetLink.from_orm(cb_link)
    db_cbl.category = db_category
    db_cbl.budget = db_budget
    session.add(db_cbl)
    session.commit()
    session.refresh(db_cbl)
    return db_cbl

def retrieve_cb_link(category_id: int, budget_id: int, session: Session = next(get_session())):
    cb_link = session.get(CategoryBudgetLink, (category_id, budget_id))
    if not cb_link:
        raise Exception('Relationship between category and budget not found')
    return cb_link

def retrieve_cb_links(session: Session = next(get_session()), offset: int = 0, limit: int = 100):
    cb_links = session.exec(select(CategoryBudgetLink).offset(offset).limit(limit)).all()
    return cb_links

def update_cb_link(category_id: int, budget_id: int, cb_link: CategoryBudgetLinkUpdate, session: Session = next(get_session())):
    db_cb_link = session.get(CategoryBudgetLink, (category_id, budget_id))
    if not db_cb_link:
        raise Exception('Relationship between category and budget not found')
    cb_link_data = cb_link.dict(exclude_unset=True)
    for key, value in cb_link_data.items():
        setattr(db_cb_link, key, value)
    session.add(db_cb_link)
    session.commit()
    session.refresh(db_cb_link)
    return db_cb_link

def delete_cb_link(category_id: int, budget_id: int, session: Session = next(get_session())):
    cb_link = session.get(CategoryBudgetLink, (category_id, budget_id))
    if not cb_link:
        raise Exception('Relationship between category and budget not found')
    session.delete(cb_link)
    session.commit()
    return {'ok': True}

