# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from typing import List

from pydantic import BaseModel

from octoconf.entities.category import Category


class Baseline(BaseModel):
    title: str
    categories: List[Category]
