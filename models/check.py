from typing import Optional

from pydantic import BaseModel


class Check(BaseModel):
    id: str
    description: str
    type: str
    cmd: str
    expected: str
    verification_type: str
    recommandation_on_failed: str
    see_also: Optional[str]


class CheckResult(BaseModel):
    id: str
    description: str
    type: str
    cmd: str
    expected: str
    verification_type: str
    cmd_output: str = ""
    result: bool = False
    recommandation_on_failed: str
    see_also: Optional[str]
