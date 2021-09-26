#!/usr/bin/env python

from abc import ABC, abstractmethod


class OutputParser(ABC):
    @abstractmethod
    def exact_match_parser(self):
        """fixme doc"""
        pass

    def regex_match_parser(self):
        """fixme doc"""
        pass
