# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import json

from octoconf.components.serializers.rule import RuleJsonEncoder
from octoconf.entities.rule import Rule


class CategoryJsonEncoder(json.JSONEncoder):
    """
    Because of the use of objects of a personality type, they are not encodable in JSON format. This class allows to encode them.
    """

    def default(self, o):
        if isinstance(o, Rule):
            return RuleJsonEncoder().default(o)
        try:
            to_serialize = {
                "category": o.category,
                "name": o.name,
                "description": o.description,
                "rules": o.rules,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
