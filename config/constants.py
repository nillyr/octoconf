#!/usr/bin/env python

import config.const as const
from sty import fg

#### PROGRAM INFO ####
const.VERSION = "v1.0.0b"

#### COLORS ####
hex2rgb = lambda x: tuple(int(x[i:i+2], 16) for i in (0, 2, 4))
const.COLORS = {
  'DARK_BLUE':'333E4E',
  'LIGHT_BLUE':'8496AF',
  'LIGT_GRAY': 'D9D9D9',
  'LIGHT_GREEN': '92D050',
  'LIGHT_ORANGE': 'F6C180',
  'LIGHT_YELLOW': 'FFFF66',
  'REGULAR_BLUE': '3891DE',
  'REGULAR_GREEN': '009644',
  'REGULAR_ORANGE': 'F1992D',
  'REGULAR_RED': 'C51718'
}

#### GETTERS ####
def get_version():
  return const.VERSION

def get_colors():
  return const.COLORS
