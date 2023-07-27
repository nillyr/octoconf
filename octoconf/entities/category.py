# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from typing import List, Optional

from pydantic import BaseModel

from octoconf.entities.rule import Rule


class Category(BaseModel):
    category: str
    name: str
    description: Optional[str]
    rules: List[Rule]
