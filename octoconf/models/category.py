# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from typing import List

from pydantic import BaseModel

from octoconf.models.checkpoint import Checkpoint


class Category(BaseModel):
    id: int
    name: str
    checkpoints: List[Checkpoint]
