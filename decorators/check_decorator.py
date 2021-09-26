#!/usr/bin/env python
from decorators.decorator import Decorator
from icecream import ic


class CheckDecorator(Decorator):
    def decorator(func):
        def inner(*args, **kwargs):
            args[1]["output"] = (
                args[1]["output"][0].rstrip(),
                args[1]["output"][1].rstrip(),
            )
            args[1]["expected"] = args[1]["expected"]
            return func(*args, **kwargs)

        return inner
