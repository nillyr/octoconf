import json

from icecream import ic

from components.json_encoders.check import CheckJsonEncoder
from components.json_encoders.checkpoint import CheckpointJsonEncoder
from components.json_encoders.checkresult import CheckResultJsonEncoder
from models import *


class ChecklistJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Checkpoint):
            return CheckpointJsonEncoder().default(o)
        if isinstance(o, Check):
            return CheckJsonEncoder().default(o)
        if isinstance(o, CheckResult):
            return CheckResultJsonEncoder().default(o)
        try:
            to_serialize = {
                "categories": [
                    {
                        "id": o.id,
                        "name": o.name,
                    }
                ]
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
