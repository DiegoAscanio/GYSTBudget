import pdb
from typing import Dict, List, Optional, Tuple, Union
from sqlalchemy.orm import session
import typer
from GYSTBudgetCLI import *
from datetime import datetime
import pandas as pd

db_session = next(get_session())
app = typer.Typer()

@app.command('transactions-as-csv')
def transactions_as_csv(csv_file : str = typer.Argument('transactions_{}.csv'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))):
    transactions = retrieve_transactions(session = db_session)
    transactions = [t.dict() for t in transactions]
    df = pd.DataFrame.from_records(transactions)
    df.to_csv(csv_file, index=False)
