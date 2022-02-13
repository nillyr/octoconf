# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoconf
# @since 1.0.0b

from abc import ABCMeta, abstractstaticmethod


class ICommandRunnerFactory(metaclass=ABCMeta):
    """
    The use of this design pattern allows to define command executors without making a spaghetti dish in the use case.
    """

    @abstractstaticmethod
    def get_runner():
        pass
