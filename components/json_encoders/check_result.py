import json


class CheckResultJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "id": o.id,
                "description": o.description,
                "type": o.type,
                "cmd": o.cmd,
                "expected": o.expected,
                "verification_type": o.verification_type,
                "cmd_output": o.cmd_output,
                "result": o.result,
                "recommandation_on_failed": o.recommandation_on_failed,
                "see_also": o.see_also if o.see_also is not None else "",
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
