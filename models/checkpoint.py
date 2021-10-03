from models.check import Check
from pydantic import BaseModel
from typing import List, Optional


class Checkpoint(BaseModel):
    id: int
    title: str
    description: str
    reference: Optional[str]
    collection_cmd: Optional[str]
    collection_cmd_type: Optional[str]
    checks: List[Check]
