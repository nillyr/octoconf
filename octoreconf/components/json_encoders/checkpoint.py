# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json

from octoreconf.components.json_encoders.check import CheckJsonEncoder
from octoreconf.components.json_encoders.checkresult import CheckResultJsonEncoder
from octoreconf.models import *


class CheckpointJsonEncoder(json.JSONEncoder):
    """
    Because of the use of objects of a personality type, they are not encodable in JSON format. This class allows to encode them.
    """

    def default(self, o):
        if isinstance(o, Check):
            return CheckJsonEncoder().default(o)
        if isinstance(o, CheckResult):
            return CheckResultJsonEncoder().default(o)
        try:
            to_serialize = {
                "id": o.id,
                "title": o.title,
                "description": o.description,
                "reference": o.reference,
                "collection_cmd": o.collection_cmd,
                "collection_cmd_type": o.collection_cmd_type,
                "collect_only": o.collect_only,
                "checks": o.checks,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
