#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

from src.models import Package

opkg_path = "/bin/opkg"


class opkg():

    @staticmethod
    def dry_run(prefix: str, packages: []):
        """
       Return a valid opkg command
       :param prefix:
       :param packages:
       :return:
       """
        if not packages and len(packages) == 0:
            if prefix == "update":
                return "{} update".format(opkg_path)
            return ""

        command = "{} {}".format(opkg_path, prefix)
        for p in packages:
            command += " {}".format(p)
        return command
