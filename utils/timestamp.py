import datetime
import time

timestamp = lambda: datetime.datetime.fromtimestamp(time.time()).strftime(
    "%Y%m%d%H%M%S"
)
