# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import json

from octoconf.components.serializers.category import CategoryJsonEncoder
from octoconf.components.serializers.rule import RuleJsonEncoder
from octoconf.entities.category import Category
from octoconf.entities.rule import Rule


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
