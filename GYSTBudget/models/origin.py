from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from models.transaction import Transaction

class OriginBase(SQLModel):
    name: str=Field(index=True)

class Origin(OriginBase, table=True):
    __table_args__ = (UniqueConstraint('name'),)
    transactions: Optional[List['Transaction']]=Relationship(
        back_populates='origin',
    )
    id : Optional[int]=Field(default=None, primary_key=True)

class OriginCreate(OriginBase):
    pass

class OriginRead(OriginBase):
    id : int

class OriginUpdate(SQLModel):
    name: Optional[str] = None

