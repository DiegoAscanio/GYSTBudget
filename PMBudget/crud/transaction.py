from models.transaction import *
from sqlmodel import Session, select
from db import get_session

def create_transaction(transaction: TransactionCreate, session: Session = next(get_session())):
    db_transaction = Transaction.from_orm(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

def retrieve_transaction(transaction_id : int, session: Session = next(get_session())):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise Exception('Transaction not found')
    return transaction

def retrieve_transactions(session: Session = next(get_session()), offset: int = 0, limit: int = 100):
    transactions = session.exec(select(Transaction).offset(offset).limit(limit)).all()
    return transactions

def update_transaction(transaction_id : int, transaction: TransactionUpdate, session: Session = next(get_session())):
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise Exception('Transaction not found')
    transaction_data = transaction.dict(exclude_unset=True)
    for key, value in transaction_data.items():
        setattr(db_transaction, key, value)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

def delete_transaction(transaction_id: int, session: Session = next(get_session())):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise Exception('Transaction not found')
    session.delete(transaction)
    session.commit()
    return {'ok': True}

