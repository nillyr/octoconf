# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from typing import List

from pydantic import BaseModel


class Rule(BaseModel):
    id: str
    title: str
    description: str = ""
    collection_cmd: str = ""
    check: str  = ""
    verification_type: str = ""
    expected: str = ""
    recommendation: str
    level: str = "minimal"
    severity: str = "unknown"
    references: List[str] = []
    # The following attributes are used when using the "analyze" command
    output: str = ""
    compliant: bool = False
