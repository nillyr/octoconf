# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from octoconf.interfaces.output_redirector_regex_abstract_builder import (
    IOutputRedirectorRegexBuilder,
)


class OutputRedirectorRegexDirector:
    """
    Class responsible for the execution of the product construction steps.
    """

    _instance = None
    _builder = None

    def __new__(cls):
        """
        Use of a singleton
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def builder(self) -> IOutputRedirectorRegexBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: IOutputRedirectorRegexBuilder) -> None:
        self._builder = builder

    def build_regex_patern(self) -> None:
        """
        Construction step to create the regex containing all the supported redirections.
        """
        self._builder.produce_redirectors()
