import sys

from icecream import ic


class Debug:
    """
    Configuration of the external package icecream.
    """
    def __init__(self) -> None:
        self.debug = False
        ic.disable()

    def set_debug(self, value: bool) -> None:
        """
        This method is called when the -d argument is present.
        """
        self.debug = value
        if self.debug:
            ic.enable()
            ic.configureOutput(prefix="Debug:", includeContext=True)
            return


sys.modules[__name__] = Debug()
