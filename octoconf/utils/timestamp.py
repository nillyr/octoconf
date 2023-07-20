# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import datetime
import time

import octoconf.utils.global_values as global_values

"""
Anonymous function to return a timestamp in YearMonthDayHourMinutesSeconds format.
"""
timestamp = lambda: datetime.datetime.fromtimestamp(time.time()).strftime(
    "%Y%m%d"
)

today = lambda: time.strftime("%d/%m/%Y" if global_values.localize.get_locale() == "FR" else "%m/%d/%Y", time.localtime())
