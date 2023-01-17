from sqlalchemy import Boolean, Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__="users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    books = relationship("Book", back_populates="owner")

class LibraryAdmin(Base):
    __tablename__="admin"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)


class Book(Base):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    quantity=Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
 
    owner = relationship("User", back_populates="books")

class LibraryAccount(Base):
    __tablename__ = "accounts"
    acc_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer)
    book_id = Column(Integer)
    date_issued = Column(DateTime(timezone=True), server_default=func.now())
    valid_till = Column(DateTime(timezone=True), server_default=func.now())
