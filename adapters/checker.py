import re

from ports.checker import IChecker


class CheckerAdapter(IChecker):
    """
    Implementation of the different verification types.
    """

    def __init__(self) -> None:
        pass

    def check_exact(self, expected, output) -> bool:
        return expected.lower() == output.lower().rstrip()

    def check_regex(self, expected, output) -> bool:
        flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
        return re.search(expected, output, flags) is not None
