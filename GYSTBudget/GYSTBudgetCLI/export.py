import pdb
from typing import Dict, List, Optional, Tuple, Union
from sqlalchemy.orm import session
import typer
from GYSTBudgetCLI import *
from datetime import datetime
import pandas as pd
import numpy as np

db_session = next(get_session())
app = typer.Typer()

def category_map(retrieved_categories = retrieve_categories(session=db_session)):
    map = {
        c.dict()['id']: c.dict()['name'] for c in retrieved_categories
    }
    map['nan'] = ''
    return map
categories = category_map()

def origin_map(retrieved_origins = retrieve_origins(session=db_session)):
    map = {
        c.dict()['id']: c.dict()['name'] for c in retrieved_origins
    }
    map['nan'] = ''
    return map
origins = origin_map()

def budget_map(retrieved_budgets = retrieve_budgets(session=db_session)):
    map = {
        c.dict()['id']: c.dict()['title'] for c in retrieved_budgets
    }
    map['nan'] = ''
    return map
budgets = budget_map()

def replace_category_id_by_name(id):
    return categories[id]

def replace_origin_id_by_name(id):
    return origins[id]

def replace_budget_id_by_name(id):
    return budgets[id]

type_enum = {
    1: 'expense',
    2: 'income'
}

def type_enum_value(value):
    return type_enum[value]

def format_date(datetime):
    return datetime.strftime('%Y-%m-%d')

@app.command('transactions-as-csv')
def transactions_as_csv(csv_file : str = typer.Argument('transactions_{}.csv'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))):
    transactions = retrieve_transactions(session = db_session)
    transactions = [t.dict() for t in transactions]
    df = pd.DataFrame.from_records(transactions)
    df['category'] = df.category_id.fillna('nan').apply(replace_category_id_by_name)
    df['origin'] = df.origin_id.fillna('nan').apply(replace_origin_id_by_name)
    df['budget'] = df.budget_id.fillna('nan').apply(replace_budget_id_by_name)
    df['type'] = df.type.apply(type_enum_value)
    df['date'] = df.date.apply(format_date)
    df = df.drop(columns=['id', 'category_id', 'origin_id', 'budget_id'])
    last_line  = pd.DataFrame.from_dict({
                'date': [datetime.now().strftime('%Y-%m-%d')],
                'type': ['summarization'],
                'budget': [''],
                'origin': [''],
                'category': [''],
                'title': ['TOTAL'],
                'amount': [df.amount.sum()]
                }
            )
    df = pd.concat(
        [
            df,
            last_line
        ]
    )
    df.to_csv(
        csv_file, 
        index=False,
        columns = ['date', 'type', 'budget', 'origin', 'category', 'title', 'amount']
    )
