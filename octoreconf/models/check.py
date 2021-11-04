# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from typing import Optional

from pydantic import BaseModel


class Check(BaseModel):
    """
    WARNING: Because the type of Category->checkpoints->check is "Check", when using components.json_encoders.checklist, cmd_output and result are needed (set them as optional in order to not fucked up with the checklist...).
    """

    id: str
    description: str
    type: str
    cmd: str
    expected: str
    verification_type: str
    cmd_output: Optional[str]
    result: Optional[bool]
    severity: str
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
    severity: str
    recommandation_on_failed: str
    see_also: Optional[str]
