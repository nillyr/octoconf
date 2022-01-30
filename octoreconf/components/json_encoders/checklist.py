# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json

from octoreconf.components.json_encoders.checkpoint import CheckpointJsonEncoder
from octoreconf.components.json_encoders.checkresult import CheckResultJsonEncoder
from octoreconf.models import *


class ChecklistJsonEncoder(json.JSONEncoder):
    """
    Because of the use of objects of a personality type, they are not encodable in JSON format. This class allows to encode them.
    """

    def default(self, o):
        if isinstance(o, Checkpoint):
            return CheckpointJsonEncoder().default(o)
        if isinstance(o, Check) or isinstance(o, CheckResult):
            # WARNING: This is only possible because Check entity has cmd_output and result variables
            return CheckResultJsonEncoder().default(o)
        try:
            to_serialize = {
                "id": o.id,
                "name": o.name,
                "checkpoints": o.checkpoints,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
