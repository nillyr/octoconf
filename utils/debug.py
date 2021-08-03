#!/usr/bin/env python

from datetime import datetime
from icecream import ic
import sys

class Debug():
  def __init__(self):
    self.debug = False

  def set_debug(self, value: bool):
    self.debug = value
    if self.debug:
      ic.configureOutput(prefix='{}:Debug:'.format(self.now()), includeContext=True)
      return
    ic.disable()

  def now(self):
    return f'[{datetime.now()}]'

sys.modules[__name__] = Debug()
