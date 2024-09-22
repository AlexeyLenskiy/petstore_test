from pydantic import BaseModel, Field
from typing import Annotated, Optional, List
from annotated_types import Gt, Ge, Len


class CategoryBody(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    
class TagBody(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    
class PetBody(BaseModel):
    id: Optional[int] = None
    category: Optional[CategoryBody] = None
    name: Optional[str] = None
    photoUrls: Optional[List[str]] = None
    tags: Optional[List[TagBody]] = None
    status: Optional[str] = None
    

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
    photoUrls: Annotated[List[Annotated[str, Len(1)]], Len(1)]  # List must have >= 1 URL, each of which must be >= 1 char
    tags: Optional[List[Tag]] = None
    status: Optional[Annotated[str, Field(r"^(available|pending|sold)$")]] = None  # Status must be: 'available', 'pending', or 'sold'
