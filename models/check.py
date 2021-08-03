#!/usr/bin/env python

from pydantic import BaseModel

class Check(BaseModel):
  id: int
  verification_type: str
  cmd: str
  expected: str
