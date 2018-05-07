#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

import unittest

from config import Configuration
from models import Package
from package_manager import PackageManager


class TestPackageMangerMethods(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.config = Configuration.load("./tmp-config.json")
        self.pm = PackageManager(self.config.package_manager_path)

    def test_install(self):
        p = Package(name="tc")

        actual = self.pm.dry_run("install", [p])
        expected = "{} install tc".format(self.config.package_manager_path)

        self.assertEqual(expected, actual)

    def test_update(self):
        actual = self.pm.dry_run("update", [])
        expected = "{} update".format(self.config.package_manager_path)

        self.assertEqual(expected, actual)

    def test_upgrade(self):
        actual = self.pm.dry_run("upgrade", [])
        expected = "{} upgrade".format(self.config.package_manager_path)

        self.assertEqual(expected, actual)

    def test_install_version(self):
        p = Package(name="tc", version="4.14.0")

        actual = self.pm.dry_run("install", [p])
        expected = "{} install tc={}".format(self.config.package_manager_path, "4.14.0")

        self.assertEqual(expected, actual)

    def test_multiple_packages(self):
        packages = [Package(name="tc"), Package(name="bash")]
        actual = self.pm.dry_run("install", packages)
        expected = "{} install tc bash".format(self.config.package_manager_path)
        self.assertEqual(expected, actual)

    def test_empty(self):
        actual = self.pm.dry_run("install", [])
        expected = ""
        self.assertEqual(expected, actual)

    def test_removal(self):
        p = Package(name="tc")

        actual = self.pm.dry_run("remove", [p])
        expected = "{} remove tc".format(self.config.package_manager_path)

        self.assertEqual(expected, actual)

        packages = [Package(name="tc"), Package(name="bash")]
        actual = self.pm.dry_run("remove", packages)
        expected = "{} remove tc bash".format(self.config.package_manager_path)
        self.assertEqual(expected, actual)

    def test_update_only(self):
        actual = self.pm.dry_run("update", [])
        expected = "{} update".format(self.config.package_manager_path)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
