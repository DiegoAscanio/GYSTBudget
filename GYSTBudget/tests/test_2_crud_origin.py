import pytest

from db import create_db_and_tables

# BEGIN ORIGIN TESTS

def test_create_db():
    create_db_and_tables()

def test_crud_create_origin() -> None :
    from sqlmodel import select
    from models.origin import Origin, OriginCreate
    from crud.origin import create_origin
    from db import get_session
    
    session = next(get_session())
    origin = OriginCreate(name = 'Origin Teste')
    create_origin(origin)
    origin_db = session.exec(select(Origin).where(Origin.name == 'Origin Teste')).first()
    assert origin_db

def test_crud_retrieve_origin() -> None:
    from crud.origin import retrieve_origin
    origin = retrieve_origin(1)
    assert origin

def test_crud_retrieve_origins() -> None:
    from crud.origin import retrieve_origins
    origins = retrieve_origins()
    assert origins

def test_crud_update_origin():
    from models.origin import OriginUpdate
    from crud.origin import update_origin
    origin_update = OriginUpdate(name = 'Nova Origem')
    db_origin = update_origin(1, origin_update)
    assert db_origin.name == 'Nova Origem' and db_origin.id == 1

def test_crud_delete_origin():
    from models.origin import OriginCreate
    from crud.origin import create_origin, delete_origin, retrieve_origin
    origin = OriginCreate(name = 'Origin a ser deletado')
    origin = create_origin(origin)
    origin_id = origin.id
    delete_origin(origin_id)
    with pytest.raises(Exception):
        retrieve_origin(origin_id)

# END ORIGIN TESTS
