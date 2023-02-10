from sqlmodel import SQLModel, Session, create_engine
from os.path import expanduser

sqlite_file_name = expanduser('~') + '/Dropbox/.gystbudget/db.sqlite3'
sqlite_url = 'sqlite:///{}'.format(sqlite_file_name)

engine = create_engine(sqlite_url, echo = True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def rollback_and_flush(session = next(get_session())):
    session.rollback()
    session.flush()
