from typing import List, Optional

from pydantic import BaseModel

from models.check import Check


class Checkpoint(BaseModel):
    id: int
    title: str
    description: str
    reference: Optional[str]
    collection_cmd: Optional[str]
    collection_cmd_type: Optional[str]
    checks: List[Check]
