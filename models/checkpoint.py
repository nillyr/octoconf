#!/usr/bin/env python

from models.check import Check

from pydantic import BaseModel
from typing import List, Optional


class Checkpoint(BaseModel):
    id: int
    title: str
    description: str
    performable: bool
    reference: Optional[str]
    level: str
    collection: str
    checks: List[Check]
    severity: str
    recommandation: str
