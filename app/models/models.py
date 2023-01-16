from sqlalchemy import Boolean, Column, Integer, PrimaryKeyConstraint, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

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
    owner_id = Column(Integer, ForeignKey("users.id"))
 
    owner = relationship("User", back_populates="books")


#not in use 
class UserLogin(Base):
    __tablename__ ="userlogin"
    login_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    class Config:
        the_schema = {
            "user_demo":{
                "email":"gaurav@gmail.com",
                "password":"123"
            }
        }   

#User Account for checking books borrowed
# class UserAccount(Base):
#     __tablename__ ="account"
#     acc_id = Column(Integer,primary_key=True, index=True )
#     Books_issued = Column(Integer, ForeignKey(Book.id))
#     Books_issued = relationship("Book", back_populates="owner")
