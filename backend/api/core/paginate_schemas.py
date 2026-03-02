from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    count: int
    next: str | None = None 
    previous: str | None = None 
    results: list[T]