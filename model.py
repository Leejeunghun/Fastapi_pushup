from datetime import datetime
from sqlite3 import Date, Timestamp, connect

from winreg import EnumKey
from sqlalchemy import Column,Integer,String,DateTime,Text,Enum,SmallInteger,Float
from pydantic import BaseModel
from db import Base
from db import ENGINE



class UserTable(Base):
    __tablename__ = 'USR'
    PK = Column(Integer,primary_key=True,autoincrement=True)
    NAME = Column(String, nullable=False)
    COUNT = Column(Integer, nullable=False)
    
class User(BaseModel):
    PK   : int
    NAME : str
    COUNT  : int

