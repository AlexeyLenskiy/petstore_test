from typing import Annotated, Any, List, Optional

from annotated_types import Ge, Len
from pydantic import BaseModel, Field


class ErrorBody(BaseModel):
    code: int
    type: str
    message: str


class CategoryBody(BaseModel):
    id: Optional[Any] = None
    name: Optional[Any] = None


class TagBody(BaseModel):
    id: Optional[Any] = None
    name: Optional[Any] = None


class PetBody(BaseModel):
    id: Optional[Any] = None
    category: Optional[CategoryBody | Any] = None
    name: Optional[Any] = None
    photoUrls: Optional[List[Any]] = None
    tags: Optional[List[TagBody | Any]] = None
    status: Optional[Any] = None


class Category(BaseModel):
    id: Optional[Annotated[int, Ge(0)]] = None  # ID must be >= 0
    name: Optional[Annotated[str, Len(1)]] = None  # Name must be >= 1 char


class Tag(BaseModel):
    id: Optional[Annotated[int, Ge(0)]] = None  # ID must be >= 0
    name: Optional[Annotated[str, Len(1)]] = None  # Name must be >= 1 char


class Pet(BaseModel):
    id: Optional[Annotated[int, Ge(0)]] = None  # ID must be >= 0
    category: Optional[Category] = None
    name: Annotated[str, Len(1)]  # Name is required and must be >= 1 char
    photoUrls: List[str | None]
    tags: Optional[List[Tag]] = None
    status: Optional[Annotated[str, Field(r"^(available|pending|sold)$")]] = (
        None  # Status must be: 'available', 'pending', or 'sold'
    )
