import pdb
from typing import Dict, List, Optional, Tuple, Union
from sqlalchemy.orm import session
import typer
from GYSTBudgetCLI import *
from datetime import datetime

app = typer.Typer()

@app.command()
def origin(name: str):
    o = OriginCreate(name = name)
    try:
        dbo = create_origin(origin=o, session = db_session)
    except Exception as e:
        rollback_and_flush(session=db_session)
        print('Error while adding {}:'.format(name))
        print(repr(e))
        sysexit(1)
    print('{} succesfully added!'.format(repr(dbo)))

@app.command()
def category(name: str):
    c = CategoryCreate(name = name)
    try:
        dbc = create_category(category=c, session = db_session)
    except Exception as e:
        rollback_and_flush(session=db_session)
        print('Error while adding {}:'.format(name))
        print(repr(e))
        sysexit(1)
    print('{} succesfully added!'.format(repr(dbc)))

_amount_or_zero= lambda amount: 0 if len(amount) == 0 else amount.pop()
def _parse_category_name_amount(category_name_amount_list):
    result = []
    for category_name_amount in category_name_amount_list:
        category, *amount = category_name_amount.split(',')
        result.append((category, _amount_or_zero(amount)))
    return result
def _build_budget(title, date = None) -> Union[BudgetCreate, None]:
        kwargs = {}
        if date:
            kwargs['date'] = date
        b = BudgetCreate(title = title, **kwargs)
        return b

def _prompt_to_confirm(o, name: str, session=db_session):
    table = {
        '<class \'models.category.Category\'>' : '''create_category(
                CategoryCreate(name = name),
                session=db_session
        )''',
        '<class \'models.origin.Origin\'>' : '''create_origin(
                OriginCreate(name = name),
                session=db_session
        )''',
        '<class \'models.budget.Budget\'>' : '''create_budget(
                                                    BudgetCreate(title = name),
                                                    session = db_session
                                                )''',
    }
    confirm = typer.confirm('{} {} not found. Do you wish to create it?'.format(repr(o), name))
    if confirm:
        return eval(table[repr(o)])
    else:
        return None

def _get_or_create_category(category_name, session=db_session):
    result = filter_categories(Category.name == category_name, session=db_session)
    if len(result) < 1:
        return category_name and _prompt_to_confirm(Category, category_name, session=db_session)
    else:
        return result.pop()

def _get_or_create_origin(origin_name, session=db_session):
    result = filter_origins(Origin.name == origin_name, session=db_session)
    if len(result) < 1:
        return origin_name and _prompt_to_confirm(Origin, origin_name, session = db_session)
    else:
        return result.pop()

def _get_or_create_budget(budget_title, session=db_session):
    result = filter_budgets(Budget.title == budget_title, session=db_session)
    if len(result) < 1:
        return budget_title and _prompt_to_confirm(Budget, budget_title, session = db_session)
    else:
        return result.pop()
 
def _create_cb_link(budget, category, amount):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=sa_exc.SAWarning)
            cb_link = create_cb_link(
                CategoryBudgetLinkCreate(
                    amount = amount
                ),
                category_id=category.id,
                budget_id=budget.id,
                session = db_session
            )
    except Exception as e:
        rollback_and_flush(session=db_session)
        print('Error while adding link between Budget {} and Category {}:'.format(budget, category))
        print(repr(e))
        sysexit(1)
    return cb_link


def _build_budget_category_name_links(budget: Budget, category_name_amount_list : List):
    links = []
    for category_name, amount in category_name_amount_list:
         category = _get_or_create_category(category_name)
         if category:
            links.append(
                _create_cb_link(
                    budget,
                    category,
                    amount,
                )
            )
    return links

# Uncomment budget on next release

'''
@app.command()
def budget(category_name_amount_list : List[str] = typer.Option(None, '--category', '-c', callback=_parse_category_name_amount), date: datetime = typer.Option(None, '--date', '-d'), title: str = typer.Argument(...)):
    budget = _build_budget(title, date)
    try:
        dbb = create_budget(budget=budget, session=db_session)
        _build_budget_category_name_links(dbb, category_name_amount_list)
        db_session.refresh(dbb)
    except Exception as e:
        rollback_and_flush(session=db_session)
        print('Error while adding {}:'.format(title))
        print(repr(e))
        sysexit(1)
    print('{} succesfully added!'.format(repr(dbb)))
'''

def _parse_transaction_category(category_name) -> Union[Category,None]:
    return _get_or_create_category(category_name)

def _parse_transaction_origin(origin_name) -> Union[Origin,None]:
    return _get_or_create_origin(origin_name)

def _parse_transaction_budget(budget_title) -> Union[Budget,None]:
    return _get_or_create_budget(budget_title)

def _build_transaction(title, amount: float, date = None, transaction_income = False) -> TransactionCreate:
    kwargs = {
        'date': date or datetime.now(),
        'type': TransactionTypeEnum(2 * transaction_income or 1),
        'amount': amount * transaction_income or amount * ~transaction_income
    }
    transaction = TransactionCreate(title=title, **kwargs)
    return transaction

_id_or_none = lambda x: x.id if x else None


# transaction with budget
'''
@app.command()
def transaction(budget = typer.Option(None, '--budget', '-b', callback=_parse_transaction_budget), origin = typer.Option(None, '--origin', '-o', callback=_parse_transaction_origin), category = typer.Option(None, '--category', '-c', callback=_parse_transaction_category), transaction_income: bool = typer.Option(False, '--income', '-i'), date : datetime = typer.Option(None, '--date', '-d'), title : str = typer.Argument(...), amount : float = typer.Argument(...)):
    transaction = _build_transaction(title = title, amount = amount, date = date, transaction_income = transaction_income)
    try:
        orm_args = {
            'budget': budget,
            'budget_id': _id_or_none(budget),
            'origin': origin,
            'origin_id': _id_or_none(origin),
            'category': category,
            'category_id': _id_or_none(category),
        }
        dbt = create_transaction(transaction = transaction, session = db_session, **orm_args)
    except Exception as e:
        rollback_and_flush(session=db_session)
        print(repr(e))
        sysexit(1)
    print('{} succesfully added!'.format(repr(dbt)))
'''

# transaction without budget

@app.command()
def transaction(origin = typer.Option(None, '--origin', '-o', callback=_parse_transaction_origin), category = typer.Option(None, '--category', '-c', callback=_parse_transaction_category), transaction_income: bool = typer.Option(False, '--income', '-i'), date : datetime = typer.Option(None, '--date', '-d'), title : str = typer.Argument(...), amount : float = typer.Argument(...)):
    transaction = _build_transaction(title = title, amount = amount, date = date, transaction_income = transaction_income)
    try:
        orm_args = {
            'origin': origin,
            'origin_id': _id_or_none(origin),
            'category': category,
            'category_id': _id_or_none(category),
        }
        dbt = create_transaction(transaction = transaction, session = db_session, **orm_args)
    except Exception as e:
        rollback_and_flush(session=db_session)
        print(repr(e))
        sysexit(1)
    print('{} succesfully added!'.format(repr(dbt)))
