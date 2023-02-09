import pytest
from db import create_db_and_tables, get_session

# BEGIN CATEGORY BUDGET LINK TESTS

def test_create_db():
    create_db_and_tables()

def test_crud_create_cb_link() -> None :
    from crud.categorybudgetlink import create_cb_link
    from models.categorybudgetlink import CategoryBudgetLinkCreate
    from models.category import Category
    from models.budget import Budget
    session = next(get_session())
    category = session.get(Category, 1)
    budget = session.get(Budget, 1)
    cb_link = CategoryBudgetLinkCreate(
        amount = 154.85
    )
    db_cb_link = create_cb_link(cb_link, category.id, budget.id, session)
    assert db_cb_link

def test_crud_retrieve_cb_link() -> None:
    from crud.categorybudgetlink import retrieve_cb_link
    cb_link = retrieve_cb_link(1, 1)
    assert cb_link

def test_crud_retrieve_cb_links() -> None:
    from crud.categorybudgetlink import retrieve_cb_links
    cb_links = retrieve_cb_links()
    assert cb_links

def test_crud_update_cb_link():
    from models.categorybudgetlink import CategoryBudgetLinkUpdate
    from crud.categorybudgetlink import update_cb_link
    from decimal import Decimal
    cb_link_update = CategoryBudgetLinkUpdate(amount = 44.95)
    db_cb_link_update = update_cb_link(1, 1, cb_link_update)
    assert db_cb_link_update.amount == Decimal('44.95')

def test_crud_delete_cb_link():
    from crud.categorybudgetlink import delete_cb_link, retrieve_cb_link
    delete_cb_link(1, 1)
    with pytest.raises(Exception):
        retrieve_cb_link(1, 1)

# END CATEGORY BUDGET LINK TESTS
