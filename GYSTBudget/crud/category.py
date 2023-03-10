from models.category import *
from db import get_session
from sqlmodel import Session, select
from typing import List
import sqlalchemy.sql.elements

def create_category(category: CategoryCreate, session: Session = next(get_session())):
    db_category = Category.from_orm(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

def retrieve_category(category_id : int, session: Session = next(get_session())):
    category = session.get(Category, category_id)
    if not category:
        raise Exception('Category not found')
    return category

def retrieve_categories(session: Session = next(get_session()), offset: int = 0, limit: int = 100):
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories

def update_category(category_id : int, category: CategoryUpdate, session: Session = next(get_session())):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise Exception('Category not found')
    category_data = category.dict(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

def delete_category(category_id: int, session: Session = next(get_session())):
    category = session.get(Category, category_id)
    if not category:
        raise Exception('Category not found')
    session.delete(category)
    session.commit()
    return {'ok': True}

def filter_categories(expression: sqlalchemy.sql.elements.BinaryExpression, session: Session=next(get_session())) -> List[Category]:
    statement = select(Category).where(expression)
    results = session.exec(statement)
    return results.all()
