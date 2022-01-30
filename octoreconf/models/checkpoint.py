# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from typing import List, Optional

from pydantic import BaseModel

from octoreconf.models.check import Check


class Checkpoint(BaseModel):
    id: int
    title: str
    description: str
    reference: Optional[str]
    collection_cmd: Optional[str]
    collection_cmd_type: Optional[str]
    collect_only: bool
    checks: Optional[List[Check]]
