# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import datetime
import time

"""
Anonymous function to return a timestamp in YearMonthDayHourMinutesSeconds format.
"""
timestamp = lambda: datetime.datetime.fromtimestamp(time.time()).strftime(
    "%Y%m%d%H%M%S"
)

today = lambda: time.strftime("%d/%m/%Y", time.localtime())
