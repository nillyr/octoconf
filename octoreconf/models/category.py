# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from typing import List

from pydantic import BaseModel

from octoreconf.models.checkpoint import Checkpoint


class Category(BaseModel):
    id: int
    name: str
    checkpoints: List[Checkpoint]
