import pytest
from db import create_db_and_tables

# BEGIN TRANSACTION TESTS

def test_create_db():
    create_db_and_tables()

def test_crud_create_transaction() -> None :
    from sqlmodel import select
    from models.transaction import Transaction, TransactionCreate, TransactionTypeEnum
    from crud.transaction import create_transaction
    from db import get_session
    
    session = next(get_session())
    transaction = TransactionCreate(title = 'Transaction Teste', type = TransactionTypeEnum.expense, amount = -54.85)
    create_transaction(transaction)
    transaction_db = session.exec(select(Transaction).where(Transaction.title == 'Transaction Teste')).first()
    assert transaction_db

def test_crud_retrieve_transaction() -> None:
    from crud.transaction import retrieve_transaction
    transaction = retrieve_transaction(1)
    assert transaction

def test_crud_retrieve_transactions() -> None:
    from crud.transaction import retrieve_transactions
    transactions = retrieve_transactions()
    assert transactions

def test_crud_update_transaction():
    from models.transaction import TransactionUpdate
    from crud.transaction import update_transaction
    transaction_update = TransactionUpdate(title = 'New Transaction')
    db_transaction = update_transaction(1, transaction_update)
    assert db_transaction.title == 'New Transaction' and db_transaction.id == 1

def test_crud_delete_transaction():
    from models.transaction import TransactionCreate, TransactionTypeEnum
    from crud.transaction import create_transaction, delete_transaction, retrieve_transaction
    transaction = TransactionCreate(title = 'Transaction a ser deletado', type = TransactionTypeEnum.income, amount = 84.95)
    transaction = create_transaction(transaction)
    transaction_id = transaction.id
    delete_transaction(transaction_id)
    with pytest.raises(Exception):
        retrieve_transaction(transaction_id)

# END TRANSACTION TESTS
