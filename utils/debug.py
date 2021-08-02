#!/usr/bin/env python

from datetime import datetime
from icecream import ic
import sys

class Debug():
  debug: bool = False
  def __init__(self, value:bool = False):
    self.debug = value

  def set_debug(self, value: bool):
    self.debug = value
    if self.debug:
      ic.configureOutput(prefix='{}:Debug:'.format(self.now()), includeContext=True)
      return
    ic.disable()

  def now(self):
    return f'[{datetime.now()}]'

sys.modules[__name__] = Debug()
