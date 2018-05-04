#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

import unittest

from src.models import Package
from src.opkg import opkg, opkg_path


class TestModelMethods(unittest.TestCase):

    def test_opkg_install(self):
        p = Package(name="tc")

        actual = opkg.install_command(p)
        expected = "{} install tc".format(opkg_path)

        self.assertEqual(expected, actual)

    def test_opkg_update(self):
        actual = opkg.update_command()
        expected = "{} update".format(opkg_path)

        self.assertEqual(expected, actual)

    def test_opkg_install_version(self):
        p = Package(name="tc", version="4.14.0")

        actual = opkg.install_command(p)
        expected = "{} install tc={}".format(opkg_path, "4.14.0")

        self.assertEqual(expected, actual)

    def test_multiple_packages(self):
        packages = [Package(name="tc"), Package(name="bash")]
        actual = opkg.install_commands(packages)
        expected = "{} install tc bash".format(opkg_path)
        self.assertEqual(expected, actual)

    def test_empty(self):
        actual = opkg.install_commands([])
        expected = ""
        self.assertEqual(expected, actual)

    # TODO: test package removal commands


if __name__ == '__main__':
    unittest.main()
