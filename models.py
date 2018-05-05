#!/usr/bin/env python3

"""
Package is the internal representation used by the daemon for generating commands.
"""


class Package:
    version: str
    name: str

    def __init__(self, name, version=None) -> None:
        self.version = version
        self.name = name

    def __str__(self) -> str:
        """
        Use a string format like the one used by opkg.
        :return: either package name or package name equals version.
        """
        if self.version:
            return "{}={}".format(self.name, self.version)
        return "{}".format(self.name)
