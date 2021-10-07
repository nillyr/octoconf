import sys

from icecream import ic


class Debug:
    def __init__(self) -> None:
        self.debug = False
        ic.disable()

    def set_debug(self, value: bool) -> None:
        self.debug = value
        if self.debug:
            ic.enable()
            ic.configureOutput(prefix="Debug:", includeContext=True)
            return


sys.modules[__name__] = Debug()
