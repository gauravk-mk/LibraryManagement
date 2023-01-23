from typing import List, Optional

from fastapi import Request

class IssuedCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.owner_email: Optional[str] = None
        self.book_title: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.owner_email = form.get("email")
        self.book_title = form.get("book_title")


    def is_valid(self):
        if not self.owner_email or not (self.owner_email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.errors:
            return True
        return False
