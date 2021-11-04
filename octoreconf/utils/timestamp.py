import datetime
import time

"""
Anonymous function to return a timestamp in YearMonthDayHourMinutesSeconds format.
"""
timestamp = lambda: datetime.datetime.fromtimestamp(time.time()).strftime(
    "%Y%m%d%H%M%S"
)
