# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from typing import List, Optional

from pydantic import BaseModel

from octoconf.entities.rule import Rule


class Category(BaseModel):
    category: str
    name: str
    description: Optional[str]
    rules: List[Rule]
