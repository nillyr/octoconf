import json

from components.json_encoders.check import CheckJsonEncoder
from components.json_encoders.checkresult import CheckResultJsonEncoder
from models import *


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
                "checks": o.checks,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
