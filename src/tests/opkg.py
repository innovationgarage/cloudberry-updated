#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

import unittest

from src.models import Package
from src.opkg import opkg, opkg_path


class TestModelMethods(unittest.TestCase):

    def test_opkg_install(self):
        p = Package(name="tc")

        actual = opkg.dry_run("install", [p])
        expected = "{} install tc".format(opkg_path)

        self.assertEqual(expected, actual)

    def test_opkg_update(self):
        actual = opkg.dry_run("update", [])
        expected = "{} update".format(opkg_path)

        self.assertEqual(expected, actual)

    def test_opkg_install_version(self):
        p = Package(name="tc", version="4.14.0")

        actual = opkg.dry_run("install", [p])
        expected = "{} install tc={}".format(opkg_path, "4.14.0")

        self.assertEqual(expected, actual)

    def test_multiple_packages(self):
        packages = [Package(name="tc"), Package(name="bash")]
        actual = opkg.dry_run("install", packages)
        expected = "{} install tc bash".format(opkg_path)
        self.assertEqual(expected, actual)

    def test_empty(self):
        actual = opkg.dry_run("install", [])
        expected = ""
        self.assertEqual(expected, actual)

    def test_opkg_remove(self):
        p = Package(name="tc")

        actual = opkg.dry_run("remove", [p])
        expected = "{} remove tc".format(opkg_path)

        self.assertEqual(expected, actual)

        packages = [Package(name="tc"), Package(name="bash")]
        actual = opkg.dry_run("remove", packages)
        expected = "{} remove tc bash".format(opkg_path)
        self.assertEqual(expected, actual)

    def test_update_only(self):
        actual = opkg.dry_run("update", [])
        expected = "{} update".format(opkg_path)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
