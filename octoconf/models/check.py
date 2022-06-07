# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from typing import Optional

from pydantic import BaseModel


class Check(BaseModel):
    """
    WARNING: Because the type of Category->checkpoints->check is "Check", when using components.json_encoders.checklist, cmd_output and result are needed (set them as optional in order to not fucked up with the checklist...).
    """

    id: str
    title: str
    description: Optional[str]
    reference: Optional[str]
    type: str
    cmd: str
    expected: str
    verification_type: str
    cmd_output: Optional[str]
    result: Optional[bool]
    level: str = "minimal"
    recommendation_on_failed: str
    see_also: Optional[str]


class CheckResult(BaseModel):
    id: str
    title: str
    description: Optional[str]
    reference: Optional[str]
    type: str
    cmd: str
    expected: str
    verification_type: str
    cmd_output: str = ""
    result: bool = False
    level: str = "minimal"
    recommendation_on_failed: str
    see_also: Optional[str]
