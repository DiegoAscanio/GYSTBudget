import pytest
from db import create_db_and_tables

# BEGIN CATEGORY TESTS

def test_create_db():
    create_db_and_tables()

def test_crud_create_category() -> None :
    from sqlmodel import select
    from models.category import Category, CategoryCreate
    from crud.category import create_category
    from db import get_session
    
    session = next(get_session())
    category = CategoryCreate(name = 'Category Teste')
    create_category(category)
    category_db = session.exec(select(Category).where(Category.name == 'Category Teste')).first()
    assert category_db

def test_crud_retrieve_category() -> None:
    from crud.category import retrieve_category
    category = retrieve_category(1)
    assert category

def test_crud_retrieve_categories() -> None:
    from crud.category import retrieve_categories
    categories = retrieve_categories()
    assert categories

def test_crud_update_category():
    from models.category import CategoryUpdate
    from crud.category import update_category
    category_update = CategoryUpdate(name = 'New Category')
    db_category = update_category(1, category_update)
    assert db_category.name == 'New Category' and db_category.id == 1

def test_crud_delete_category():
    from models.category import CategoryCreate
    from crud.category import create_category, delete_category, retrieve_category
    category = CategoryCreate(name = 'Category a ser deletado')
    category = create_category(category)
    category_id = category.id
    delete_category(category_id)
    with pytest.raises(Exception):
        retrieve_category(category_id)

# END CATEGORY TESTS
