from panther.db import Model

class Book(Model):
    name: str
    author: str
    pages_count: int
