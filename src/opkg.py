#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

from src.models import Package

opkg_path = "/bin/opkg"


class opkg():
    @staticmethod
    def install_command(p: Package):
        if p.version: return "{} install {}".format(opkg_path, p)

        return "{} install {}".format(opkg_path, p)

    @classmethod
    def update_command(cls):
        return "{} update".format(opkg_path)

    @classmethod
    def install_commands(cls, packages):
        if len(packages) == 0:
            return ""

        command = "{} install".format(opkg_path)
        for p in packages:
            command += " {}".format(p)
        return command
