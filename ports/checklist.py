#!/usr/bin/env python

from abc import ABC, abstractmethod


class Checklist(ABC):
    @abstractmethod
    def checklist_parser(self, filename):
        """fixme doc"""
        pass
