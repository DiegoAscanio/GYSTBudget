from db import get_session, rollback_and_flush, create_db_and_tables
from models.origin import *
from models.category import *
from models.budget import *
from models.categorybudgetlink import *
from models.transaction import *
from crud.origin import *
from crud.category import *
from crud.budget import *
from crud.categorybudgetlink import *
from crud.transaction import *
from sys import exit as sysexit
import logging
import sqlalchemy.exc as sa_exc
import warnings

# disable sqlalchemy logging
logging.disable(logging.INFO)

# 1. this will be removed when we implement alembic migrations
create_db_and_tables()

db_session = next(get_session())
