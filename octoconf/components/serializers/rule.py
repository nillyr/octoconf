# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import json


class RuleJsonEncoder(json.JSONEncoder):
    """
    Because of the use of objects of a personality type, they are not encodable in JSON format. This class allows to encode them.
    """

    def default(self, o):
        try:
            to_serialize = {
                "id": o.id,
                "title": o.title,
                "description": o.description,
                "collection_cmd": o.collection_cmd,
                "check": o.check,
                "verification_type": o.verification_type,
                "expected": o.expected,
                "recommendation": o.recommendation,
                "level": o.level,
                "severity": o.severity,
                "references": o.references,
                "output": o.output,
                "compliant": o.compliant,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
