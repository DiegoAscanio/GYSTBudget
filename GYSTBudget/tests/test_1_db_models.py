import pytest
import pdb
import os

from models.category import Category
from models.budget import Budget
from models.categorybudgetlink import CategoryBudgetLink
from models.origin import Origin
from models.transaction import Transaction

exists = os.path.exists
wdir = os.getcwd() 
def test_1_df_files_exists() -> None:
    exports_dir = wdir + '/exports/'
    filenames = [exports_dir + name for name in ['expenses-current-month.json', 'expenses-current-month.csv', 'budget.json', 'budget.csv']]
    for filename in filenames:
        assert exists(filename)

def test_db() -> None:
    # delete db if exists
    dbf = wdir + '/db.sqlite3'
    if exists(dbf):
        os.remove(dbf)
    import db
    from sqlalchemy.engine import Inspector
    from sqlmodel import inspect
    db.create_db_and_tables()
    insp: Inspector = inspect(db.engine)
    assertions = [
        insp.has_table(str(Category.__tablename__)),
        insp.has_table(str(Budget.__tablename__)),
        insp.has_table(str(CategoryBudgetLink.__tablename__)),
        insp.has_table(str(Origin.__tablename__)),
        insp.has_table(str(Transaction.__tablename__))
    ]
    for assertion in assertions:
        assert assertion

def test_category_origin_transaction_models() -> None:
    from datetime import datetime
    from models.category import Category
    from models.origin import Origin
    from models.transaction import Transaction, TransactionTypeEnum

    category = Category(
        id = 2,
        name = 'C2'
    )

    origin = Origin(
        id = 2,
        name = 'O2'
    )

    transaction = Transaction (
        id = 2,
        type = TransactionTypeEnum.expense,
        date = datetime.now(),
        category_id = category.id,
        origin_id = origin.id,
        title = 'T2',
        amount = -5
    )

    model_assertions = {
        'category': category.__fields_set__ == {'id', 'name'},
        'origin': origin.__fields_set__ == {'id', 'name'},
        'transaction': transaction.__fields_set__ == {'id', 'type', 'date', 'title', 'amount', 'category_id', 'origin_id' }
    }

    for model in model_assertions:
        assert model_assertions[model]


def test_budget_and_category_models():
    from datetime import datetime
    from models.category import Category
    from models.budget import Budget
    from models.categorybudgetlink import CategoryBudgetLink

    category = Category(
        id = 3,
        name = 'test-category'
    )

    budget = Budget(
        id = 3,
        title = 'test-budget',
        date = datetime.now()
    )

    cblink = CategoryBudgetLink(
        budget = budget,
        category = category,
        amount = 100,
        category_id = category.id,
        budget_id = budget.id
    )

    model_assertions = {
        'category': category.__fields_set__ == {'id', 'name'},
        'budget': budget.__fields_set__ == {'id', 'title', 'date'},
        'categorybudgetlink': cblink.__fields_set__ == {'amount', 'category_id', 'budget_id' }
    }

    for model in model_assertions:
        assert model_assertions[model]
