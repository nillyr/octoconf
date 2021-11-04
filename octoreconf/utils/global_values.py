# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from octoreconf.utils import Locale


def set_localize(lang: str):
    global localize
    localize = Locale(lang)
