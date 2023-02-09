import pdb
from typing import Dict, List, Optional, Tuple, Union
from sqlalchemy.orm import session
import typer
from GYSTBudgetCLI import *
from datetime import datetime

db_session = next(get_session())
app = typer.Typer()

@app.command()
def origin(name: str):
    result = filter_origins(Origin.name == name, session = db_session)
    if len(result) == 0:
        print('Origin {} doesn\'t exist'.format(name))
        sysexit(1)

    origin = result.pop()
    try:
        status = delete_origin(origin.id, session=db_session)
        print('Origin {} deleted'.format(name))
    except Exception as e:
        print('An error happened during origin {} deletion'.format(name))
        print(repr(e))
        sysexit(1)

@app.command()
def category(name: str):
    result = filter_categories(Category.name == name, session = db_session)
    if len(result) == 0:
        print('Category {} doesn\'t exist'.format(name))
        sysexit(1)

    category = result.pop()
    try:
        status = delete_category(category.id, session=db_session)
        print('Category {} deleted'.format(name))
    except Exception as e:
        print('An error happened during category {} deletion'.format(name))
        print(repr(e))
        sysexit(1)

@app.command()
def budget(title: str):
    result = filter_budgets(Budget.title == title, session = db_session)
    if len(result) == 0:
        print('Budget {} doesn\'t exist'.format(title))
        sysexit(1)

    budget = result.pop()
    try:
        status = delete_budget(budget.id, session=db_session)
        print('Budget {} deleted'.format(title))
    except Exception as e:
        print('An error happened during budget {} deletion'.format(title))
        print(repr(e))
        sysexit(1)


def _confirm_transaction_deletion(transaction):
    confirm = typer.confirm('Do you really wish to delete transaction {}?'.format(repr(transaction)))
    if confirm:
        return transaction
    else:
        return None

@app.command()
def transaction(title: str):
    to_delete = []
    result = filter_transactions(Transaction.title == title, session = db_session)
    if len(result) == 0:
        print('Transaction {} doesn\'t exist'.format(title))
        sysexit(1)
    elif len(result) > 1:
        print('Two or more transactions with the same title were found')
        for transaction in result:
            transaction = _confirm_transaction_deletion(transaction)
            if transaction:
                to_delete.append(transaction)
    else:
        to_delete.append(result.pop())
    try:
        for transaction in to_delete:
            delete_transaction(transaction.id, session = db_session)
            print('Transaction {} deleted'.format(repr(transaction)))
    except Exception as e:
        print('Error while deleting transaction {}'.format(repr(transaction)))
        print(repr(e))
        sysexit(1)
