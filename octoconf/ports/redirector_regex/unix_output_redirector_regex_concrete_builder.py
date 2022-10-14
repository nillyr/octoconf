# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from enum import Enum

from octoconf.adapters.redirector_regex.output_redirector_regex_product import (
    OutputRedirectorRegexProduct,
)
from octoconf.ports.redirector_regex.output_redirector_regex_abstract_builder import (
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

        BASICS = r"(?<!\$\.)\s*(?<!2)>+\s*(?!=|\&)(?#[a-zA-Z0-9.\-_/]+)(?#(;|&&)"
        FILE_DESCRIPTORS_ADDITIONAL_FILES = r"[3-9]<>(?#[a-zA-Z0-9.\-_/]+)(?#(;|&&)"

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
