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
        # DO NOT REMOVE THE FLAG "DOTALL"
        # https://docs.python.org/3/library/re.html#re.DOTALL
        flags = re.DOTALL | re.IGNORECASE
        return re.match(expected, output, flags) is not None
