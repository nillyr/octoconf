# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from octoconf.utils.locale.locale import Locale


def set_localize(lang: str):
    global localize
    localize = Locale(lang)


def get_locale() -> str:
    return localize.get_locale()
