# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import json

from octoconf.components.serializers.category import CategoryJsonEncoder
from octoconf.components.serializers.rule import RuleJsonEncoder
from octoconf.entities import Category, Rule


class BaselineJsonEncoder(json.JSONEncoder):
    """
    Because of the use of objects of a personality type, they are not encodable in JSON format. This class allows to encode them.
    """

    def default(self, o):
        if isinstance(o, Category):
            return CategoryJsonEncoder().default(o)
        if isinstance(o, Rule):
            return RuleJsonEncoder().default(o)
        try:
            to_serialize = {
                "title": o.title,
                "categories": o.categories
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
