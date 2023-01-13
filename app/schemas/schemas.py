from typing import List, Union

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    description: Union[str, None] = None


class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int

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