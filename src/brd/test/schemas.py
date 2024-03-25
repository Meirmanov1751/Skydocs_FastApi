from pydantic import BaseModel
from typing import List

class ItemRequest(BaseModel):
    name: str
    description: str
    price: float
    tax: float


class ItemDelete(BaseModel):
    id: int


class DeleteItemsRequest(BaseModel):
    ids: List[int]
