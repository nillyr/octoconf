# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from enum import Enum

from octoconf.interface_adapters.redirector_regex.output_redirector_regex_product import (
    OutputRedirectorRegexProduct,
)
from octoconf.interfaces.output_redirector_regex_abstract_builder import (
    IOutputRedirectorRegexBuilder,
)


class NoValue(Enum):
    """
    Enables to set the enumeration values in string form and thus reduce the number of lines of code.
    """

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)


class UnixOutputRedirectorRegexCB(IOutputRedirectorRegexBuilder):
    """
    Concrete builder for Linux/Unix allowing to create a regex with all supported redirections.
    """

    class RedirectorsRegexEnum(NoValue):
        """
        Set of supported redirections.
        """

        # [fd (fd!= 2)]>[>] output_file
        BASICS = r"\s*\d?(?<!2)\&?>{1,2}\|?(?!\&)\s*"
        # Do not match fd to fd (exec 3>&1) or input to fd (exec 3<input_file)
        FD_TO_FILES = r"(?#exec)\s+\d(?:(?:<?>))(?!\&)"
        # Bash commands
        TEE_CMD = r"\|\s*tee\s+(?:-(?:[a-z]\s*))*"

    _instance = None
    _product = None

    def __new__(cls):
        """
        Use of a singleton
        """
        if cls._instance is None:
            cls._product = OutputRedirectorRegexProduct()
            cls._instance = super().__new__(cls)
        return cls._instance

    def reset(self) -> None:
        """
        Dead code at least for now.
        """
        self._product = OutputRedirectorRegexProduct()

    @property
    def product(self) -> OutputRedirectorRegexProduct:
        """
        Getter of the "final" product.
        """
        return self._product

    def produce_redirectors(self) -> None:
        """
        Producer to build the product.
        """
        [self._product.add(x.value) for x in self.RedirectorsRegexEnum]
