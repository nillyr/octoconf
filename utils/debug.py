#!/usr/bin/env python

from icecream import ic
import sys

class Debug():
  def __init__(self):
    self.debug = False
    ic.disable()

  def set_debug(self, value: bool):
    self.debug = value
    if self.debug:
      ic.enable()
      ic.configureOutput(prefix='Debug:', includeContext=True)
      return

sys.modules[__name__] = Debug()
