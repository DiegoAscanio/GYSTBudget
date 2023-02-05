import pdb
from models.transaction import *
from models.origin import *
from models.category import *
from models.budget import *
from models.categorybudgetlink import CategoryBudgetLinkCreate
from crud.categorybudgetlink import create_cb_link
from crud.category import create_category
from crud.budget import create_budget, retrieve_budget
from db import *
from numpy.random import randint
from datetime import datetime

create_db_and_tables()
session = next(get_session())

category = CategoryCreate(
    name = 'Category {}'.format(str(randint(0,2**32)))
)
category = create_category(category)

budget = retrieve_budget(1)

cbl = CategoryBudgetLinkCreate(
    amount = randint(1, 2**16)
)

dbcbl = create_cb_link(cbl, category_id=category.id, budget_id=budget.id)
