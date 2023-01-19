from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import datetime
from sqlalchemy.orm import relationship
# as_declarative()  is a class decorator for declarative_base()
# declared_attr marks a class-level method as representing the definition of a mapped property or special declarative member name.
@as_declarative()
class Base:
    id: Any
    _name_: str
    # to generate tablename from classname
    @declared_attr
    def created_on(cls):
        return Column(DateTime(timezone=True), server_default=func.now())
    @declared_attr
    def modified_on(cls):
        return Column(DateTime(timezone=True), onupdate=func.now())
    @declared_attr
    def created_by(cls):
        return Column(Integer, ForeignKey("users.name"))
    @declared_attr
    def modified_by(cls):   
        return Column(Integer, ForeignKey("users.name"))

    