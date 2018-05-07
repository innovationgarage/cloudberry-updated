#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

import unittest

from models import Package
from package_manager import PackageManager, package_manager_path


class TestPackageMangerMethods(unittest.TestCase):

    def test_install(self):
        p = Package(name="tc")

        actual = PackageManager.dry_run("install", [p])
        expected = "{} install tc".format(package_manager_path)

        self.assertEqual(expected, actual)

    def test_update(self):
        actual = PackageManager.dry_run("update", [])
        expected = "{} update".format(package_manager_path)

        self.assertEqual(expected, actual)

    def test_upgrade(self):
        actual = PackageManager.dry_run("upgrade", [])
        expected = "{} upgrade".format(package_manager_path)

        self.assertEqual(expected, actual)

    def test_install_version(self):
        p = Package(name="tc", version="4.14.0")

        actual = PackageManager.dry_run("install", [p])
        expected = "{} install tc={}".format(package_manager_path, "4.14.0")

        self.assertEqual(expected, actual)

    def test_multiple_packages(self):
        packages = [Package(name="tc"), Package(name="bash")]
        actual = PackageManager.dry_run("install", packages)
        expected = "{} install tc bash".format(package_manager_path)
        self.assertEqual(expected, actual)

    def test_empty(self):
        actual = PackageManager.dry_run("install", [])
        expected = ""
        self.assertEqual(expected, actual)

    def test_removal(self):
        p = Package(name="tc")

        actual = PackageManager.dry_run("remove", [p])
        expected = "{} remove tc".format(package_manager_path)

        self.assertEqual(expected, actual)

        packages = [Package(name="tc"), Package(name="bash")]
        actual = PackageManager.dry_run("remove", packages)
        expected = "{} remove tc bash".format(package_manager_path)
        self.assertEqual(expected, actual)

    def test_update_only(self):
        actual = PackageManager.dry_run("update", [])
        expected = "{} update".format(package_manager_path)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
