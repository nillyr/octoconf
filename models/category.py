from typing import List

from pydantic import BaseModel

from models.checkpoint import Checkpoint

class Category(BaseModel):
    id: int
    name: str
    checkpoints: List[Checkpoint]
