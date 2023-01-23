from typing import List, Union, Optional
from datetime import date, timedelta, datetime
from pydantic import BaseModel, EmailStr


# class appBase(BaseModel):
#     created_by: int
#     created_on: str
#     modified_by: int
#     modified_on: str


class BookBase(BaseModel):
    title: Optional[str] 
    author: Optional[str] 
    quantity: Optional[str] 
    description: Optional[str] 


class BookCreate(BookBase):
    pass
    
class Book(BookBase):
    class Config:
        orm_mode = True

class ShowBook(Book):
    title: str
    author: str
    description:str
    quantity: int

    class Config:
        orm_mode = True




class UserBase(BaseModel):
    email: str


class UserCreatedefault(BaseModel):
    name : str
    password: str
    email: str


class UserCreate(UserCreatedefault):
    created_by: str
    created_on: date
    modified_by: str
    modified_on: date


class UserLoginSchema(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    books: List[Book] = []
    password: str

    class Config:
        orm_mode = True


class LibraryAccountBase(BaseModel):
    book_title :Optional[str] = None
    owner_email:str

class LibraryAcoount(LibraryAccountBase):
    date_issued: Optional[date] = datetime.now().date()
    valid_till : Optional[date] = datetime.now().date() + timedelta(days=15)
    class Config:
        orm_mode = True
  
class ShowLibraryAcoount(LibraryAccountBase):
    date_issued: Optional[date] = datetime.now().date()
    valid_till: Optional[date] = datetime.now().date() + timedelta(days=15)
    actual_return_date: Optional[date] = datetime.now().date()
    
    class Config:  # to convert non dict obj to json
        orm_mode = True

class UpdateAccount(LibraryAccountBase):
    actual_return_date: Optional[str] = datetime.now().date()




class Token(BaseModel):
    access_token: str
    token_type: str
