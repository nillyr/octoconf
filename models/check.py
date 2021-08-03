#!/usr/bin/env python

from pydantic import BaseModel
from typing import Optional

class Check(BaseModel):
  id: int
  output_path: Optional[str]
  output_file: Optional[str]
  verification_type: Optional[str]
  cmd: str
  expected: Optional[str]
