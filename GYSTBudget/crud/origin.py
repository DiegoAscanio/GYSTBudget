from sqlite3 import IntegrityError
from models.origin import *
from sqlmodel import Session, select
from db import get_session
from typing import List
import sqlalchemy.sql.elements

def create_origin(origin: OriginCreate, session: Session = next(get_session())):
    db_origin = Origin.from_orm(origin)
    try:
        session.add(db_origin)
        session.commit()
        session.refresh(db_origin)
    except:
        session.rollback()
        raise
    return db_origin

def retrieve_origin(origin_id : int, session: Session = next(get_session())):
    origin = session.get(Origin, origin_id)
    if not origin:
        raise Exception('Origin not found')
    return origin

def retrieve_origins(session: Session = next(get_session()), offset: int = 0, limit: int = 100):
    origins = session.exec(select(Origin).offset(offset).limit(limit)).all()
    return origins

def update_origin(origin_id : int, origin: OriginUpdate, session: Session = next(get_session())):
    db_origin = session.get(Origin, origin_id)
    if not db_origin:
        raise Exception('Origin not found')
    origin_data = origin.dict(exclude_unset=True)
    for key, value in origin_data.items():
        setattr(db_origin, key, value)
    session.add(db_origin)
    session.commit()
    session.refresh(db_origin)
    return db_origin

def delete_origin(origin_id: int, session: Session = next(get_session())):
    origin = session.get(Origin, origin_id)
    if not origin:
        raise Exception('Origin not found')
    session.delete(origin)
    session.commit()
    return {'ok': True}

def filter_origins(expression: sqlalchemy.sql.elements.BinaryExpression, session: Session=next(get_session())) -> List[Origin]:
    statement = select(Origin).where(expression)
    results = session.exec(statement)
    return results.all()
