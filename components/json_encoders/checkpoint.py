import json


class CheckpointJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "id": o.id,
                "title": o.title,
                "description": o.description,
                "collection_cmd": o.collection_cmd,
                "collection_cmd_type": o.collection_cmd_type,
                "checks": o.checks,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
