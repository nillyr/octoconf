# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from octoconf.interface_adapters.redirector_regex.output_redirector_regex_director import (
    OutputRedirectorRegexDirector,
)
from octoconf.interface_adapters.redirector_regex.unix_output_redirector_regex_concrete_builder import (
    UnixOutputRedirectorRegexCB,
)
from octoconf.interface_adapters.redirector_regex.windows_output_redirector_regex_concrete_builder import (
    WindowsOutputRedirectorRegexCB,
)


class RedirectorRegex:
    """
    Class working in the same way as a factory allowing to get the "compiled" regex with all the supported redirections for a given system.
    """

    @staticmethod
    def get_redirector_regex(platform) -> str:
        """
        Returns a "compiled" regex with all supported redirects.
        """
        # As this method can be called many times, I use singletons in the called classes.
        director = OutputRedirectorRegexDirector()
        # Unix is not a value that can be returned by platform.system().
        # Yet, the class where thi word is used is itself named "Unix...".
        # Therefore, this is tolerated.
        if platform in ("Darwin", "Linux", "Unix"):
            builder = UnixOutputRedirectorRegexCB()
        elif platform == "Windows":
            builder = WindowsOutputRedirectorRegexCB()

        director.builder = builder
        director.build_regex_patern()
        return builder.product.get_redirector_regex()
