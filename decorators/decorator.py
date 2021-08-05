#!/usr/bin/env python

from abc import ABC, abstractmethod

class Decorator(ABC):
  @abstractmethod
  def decorator(func):
    """ fixme doc """
    pass
