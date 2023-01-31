import pytest
import pandas as pd
import os

def test_1_df_files_exists():
    wdir = '/home/diego/Dropbox/ordenando_2023/orcamento_2023/PMBudget/PMBudget/PMBudget/'
    exists = os.path.exists
    filenames = [wdir + name for name in ['expenses-current-month.json', 'expenses-current-month.csv', 'budget.json', 'budget.csv']]
    for filename in filenames:
        assert exists(filename)
