# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

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


class WindowsOutputRedirectorRegexCB(IOutputRedirectorRegexBuilder):
    """
    Concrete builder for Windows allowing to create a regex with all supported redirections.
    See also: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.2
    """

    class RedirectorsRegexEnum(NoValue):
        """
        Set of supported redirections.
        """

        BASICS = r"(?:\s*(?:\d?|\*)>{1,2}(?!\&)\s*)(?![^efhilorsw\(]*\))"
        CMD_GPRESULT = r"\s*/H\s*"
        CMD_SECEDIT = r"\s*/cfg\s*"
        CMD_MSINFO32 = r"\s*/report\s*"
        CMDLET_EXPORT_CSV = r"\s*\|\s*Export-CSV\s+(?:-[a-zA-Z]*\s*(?:utf8\s*)*)*"
        CMDLET_OUT_FILE = r"\s*\|\s*Out-File\s+(?:-[a-zA-Z]*\s*(?:utf8\s*)*)*"
        CMDLET_TEE_OBJECT = r"\s*\|\s*Tee-Object\s+(?:-(?:InputObject\s*|Variable\s*|[a-zA-Z\$])*\s*(?:utf8\s*)*)*"

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
