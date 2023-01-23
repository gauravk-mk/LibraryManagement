from sqlalchemy import Boolean, Column, Integer, DateTime, String, ForeignKey
from datetime import date, timedelta
from sqlalchemy.orm import relationship
from .base_class import Base
# from app.database import Base
from sqlalchemy.sql import func

#to add log's column in every table ? 

class User(Base):
    __tablename__="users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)



class Book(Base):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    author = Column(String)
    description = Column(String)
    quantity=Column(Integer)
    # owner_id = Column(Integer, ForeignKey("users.id"))
 
    # owner = relationship("User", back_populates="books")


class LibraryAccount(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    owner_email = Column(String, ForeignKey("users.email"))
    book_title = Column(String, ForeignKey("books.title"))
    date_issued = Column(String)
    valid_till = Column(String)
    actual_return_date = Column(String)


# class LibraryAdmin(Base):
#     __tablename__="admin"
#     __table_args__ = {'extend_existing': True}

#     id = Column(Integer, primary_key=True,index=True)
#     email = Column(String, unique=True, index=True)
#     name = Column(String)
#     hashed_password = Column(String)


