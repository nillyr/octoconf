# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from typing import Any


class OutputRedirectorRegexProduct:
    """
    Concrete product allowing to create a list of redirections then concatenates the elements by adding the logical OR (|).
    """

    def __init__(self) -> None:
        self.redirectors = []

    def add(self, redirector: Any) -> None:
        """
        Add a redirection to the list.
        """
        self.redirectors.append(redirector)

    def get_redirector_regex(self) -> str:
        """
        Concatenates redirections with a logical OR (|).
        """
        return "|".join(self.redirectors)
