from typing import List, Optional

from fastapi import Request


class BookCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.id: int
        self.title: Optional[str]
        self.author: Optional[str]
        self.description: Optional[str] 
        self.quantity: Optional[int] 

    async def load_data(self):
        form = await self.request.form()
        self.id = form.get("id")
        self.title = form.get("title")
        self.author = form.get("author")
        self.description = form.get("description")
        self.quantity = form.get("quantity")

    def is_valid(self):
        if not self.title or not len(self.title) >= 4:
            self.errors.append("A valid title is required")
        if not self.description or not len(self.description) >= 5:
            self.errors.append("Description too short")
        if not self.errors:
            return True
        return False
