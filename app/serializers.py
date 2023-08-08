from pydantic import BaseModel

class BookSerializer(BaseModel):
    name: str
    author: str
    pages_count: int

class BookOutputSerializer(BaseModel):
    name: str
    pages_count: int
