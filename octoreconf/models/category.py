from typing import List

from pydantic import BaseModel

from octoreconf.models.checkpoint import Checkpoint


class Category(BaseModel):
    id: int
    name: str
    checkpoints: List[Checkpoint]
