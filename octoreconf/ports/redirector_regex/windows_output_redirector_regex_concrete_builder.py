# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from enum import Enum

from octoreconf.adapters.redirector_regex.output_redirector_regex_product import (
    OutputRedirectorRegexProduct,
)
from octoreconf.ports.redirector_regex.output_redirector_regex_abstract_builder import (
    IOutputRedirectorRegexBuilder,
)


class NoValue(Enum):
    """
    Enables to set the enumeration values in string form and thus reduce the number of lines of code.
    """

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)


class WindowsOutputRedirectorRegexCB(IOutputRedirectorRegexBuilder):
    """
    Concrete builder for Windows allowing to create a regex with all supported redirections.
    See also: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.2
    """

    class RedirectorsRegexEnum(NoValue):
        """
        Set of supported redirections.
        """

        DEFAULT = "\s*>+\s*"
        OUT_FILE_CMDLET = (
            "\s*\|\s*Out-File\s+-Encoding\s+utf8\s+(-(Append|FilePath)\s+)*"
        )
        GPRESULT = "\s*/H\s*"
        SECEDIT = "\s*/cfg\s*"

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
