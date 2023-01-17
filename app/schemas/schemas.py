from typing import List, Union
from datetime import date, timedelta
from pydantic import BaseModel


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
    date_issued = date.isoformat(date.today())
    valid_till = date.isoformat(date.today() + timedelta(days=15))

    class Config:
        orm_mode = True
  
