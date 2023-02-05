from db import Session, engine, select
from typing import Any, List
import pdb

class CRUD():
 
    def __config__(self):
        pass
    def save(self: Any):
        with Session(engine) as session:
            session.add(self)
            session.commit()

    def delete(self: Any):
        with Session(engine) as session:
            statement = select(self.__class__).where(self.__class__.id == self.id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()

    class objects():
        def delete(self, object: Any, *args, **kwargs):
            pass
        def _filter(self, *args, **kwargs) -> Any:
            pass
        def filter(self, object: Any, *args, **kwargs) -> List[Any]:
            return []
        def update(self, object: Any, *args, **kwargs) -> Any:
            pass
