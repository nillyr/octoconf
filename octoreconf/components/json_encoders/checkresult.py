# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json


class CheckResultJsonEncoder(json.JSONEncoder):
    """
    Because of the use of objects of a personality type, they are not encodable in JSON format. This class allows to encode them.
    """

    def default(self, o):
        try:
            to_serialize = {
                "id": o.id,
                "title": o.title if o.title is not None else "",
                "description": o.description,
                "type": o.type,
                "cmd": o.cmd,
                "expected": o.expected,
                "verification_type": o.verification_type,
                "cmd_output": o.cmd_output,
                "result": o.result,
                "severity": o.severity,
                "recommandation_on_failed": o.recommandation_on_failed,
                "see_also": o.see_also if o.see_also is not None else "",
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
