from typing import List, Union
from datetime import date, timedelta, datetime
from pydantic import BaseModel


class appBase(BaseModel):
    created_by: int
    created_on: date



class BookBase(BaseModel):
    title: str
    description: Union[str, None] = None


class BookCreate(BookBase):
    pass
    
class Book(BookBase):
    id: int
    quantity:int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name : str
    password: str

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
    book_id :int
    owner_id:int

class LibraryAcoount(LibraryAccountBase):
    acc_id : int
    user_name: str
    date_issued = str
    valid_till = str

    class Config:
        orm_mode = True
  