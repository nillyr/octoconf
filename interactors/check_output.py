#!/usr/bin/env python

from decorators.check_decorator import CheckDecorator
from icecream import ic
from ports.output_parser import OutputParser
import datetime
import json
import re
import time


class CheckOutputInteractor(OutputParser):
    __timestamp = lambda _: datetime.datetime.fromtimestamp(time.time()).strftime(
        "%Y%m%d%H%M%S"
    )

    def __init__(self, adapter):
        self.adapter = adapter

    def exact_match_parser(self, expected, output):
        ic(expected, output)
        return expected.lower() == output.lower()

    def regex_match_parser(self, expected, output):
        # DO NOT REMOVE THE FLAG "DOTALL"
        # https://docs.python.org/3/library/re.html#re.DOTALL
        ic(expected, output)
        flags = re.DOTALL | re.IGNORECASE
        return re.match(expected, output, flags) is not None

    @CheckDecorator.decorator
    def __check_output(self, check):
        # If there is nothing on stdout, check failed by default
        if not check["output"][0]:
            check["result"] = False
            return check

        if check["verification_type"] == "regex match":
            check["result"] = self.regex_match_parser(
                check["expected"], check["output"][0]
            )
        else:
            check["result"] = self.exact_match_parser(
                check["expected"], check["output"][0]
            )
        return check

    def __get_check(self, categories, cmd_id):
        category_id, checkpoint_id, check_id = (
            int(cmd_id.split(".")[0]),
            int(cmd_id.split(".")[1]),
            int(cmd_id.split(".")[2]),
        )
        check = (
            categories[category_id - 1]
            .checkpoints[checkpoint_id - 1]
            .checks[check_id - 1]
        )
        return ic(check)

    def execute(self, checklist, results):
        categories = self.adapter.checklist_parser(checklist)
        checks = []
        for cmds_list in results:
            for cmd in cmds_list:
                check = self.__get_check(categories, cmd["cmd_id"])
                result = self.__check_output(
                    {
                        "cmd_id": cmd["cmd_id"],
                        "verification_type": check.verification_type,
                        "output": cmd["output"],
                        "expected": check.expected,
                        "result": "N/A",
                    }
                )
                checks.append(result)

        with open(self.__timestamp() + "_checkoutput_results.json", "w") as json_file:
            json.dump(checks, json_file)

        return ic(checks)
