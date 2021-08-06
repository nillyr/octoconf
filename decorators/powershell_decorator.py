#!/usr/bin/env python

from decorators.decorator import Decorator


class PowershellDecorator(Decorator):
    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            # TODO: add commands: create directory, get timestamp, check permissions
            content.append("TODO: prolog")
            content.extend(func(*args, **kwargs))
            # TODO: add finish timestamp and zip
            content.append("TODO: epilog")
            return content

        return inner
