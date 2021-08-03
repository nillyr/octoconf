#!/usr/bin/env python

from models.checkpoint import Checkpoint

from pydantic import BaseModel
from typing import List

class Category(BaseModel):
  id: int
  name: str
  checkpoints: List[Checkpoint]
