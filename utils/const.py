#!/usr/bin/env python

import sys


class Const(object):
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("A constant cannot be rebind")
        self.__dict__[name] = value


sys.modules[__name__] = Const()
