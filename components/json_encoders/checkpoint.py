import json


class CheckpointJsonEncoder(json.JSONEncoder):
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
                "collection_cmd_type": o.collection_cmd_type,
                "checks": o.checks,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
