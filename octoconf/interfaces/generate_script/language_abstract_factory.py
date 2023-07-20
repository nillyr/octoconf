# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from abc import ABCMeta, abstractstaticmethod


class ILanguageFactory(metaclass=ABCMeta):
    """
    The use of this design pattern makes it possible to define many systems without having to modify a large part of the source code of the use cases.
    """

    @abstractstaticmethod
    def get_language(language_name):
        pass
