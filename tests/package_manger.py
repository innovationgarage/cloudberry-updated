#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

import unittest

from config import Configuration
from models import Package
from package_manager import PackageManager


class TestPackageMangerMethods(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.config = Configuration.load("./configs/example_updated_config.uci")
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

    def test_list_installed(self):
        opkg_output = """
nano - 2.7.5-1
opkg - 2017-03-23-1d0263bb-1
        """
        expected = {'nano': '2.7.5-1', 'opkg': '2017-03-23-1d0263bb-1'}
        actual = self.pm.list_installed_to_dict(opkg_output)

        self.assertEqual(expected, actual)

    def test_local_install_format(self):
        expected = {'nano': '2.7.5-1', 'opkg': '2017-03-23-1d0263bb-1'}
        actual = self.pm.load_local_packages_list("./configs/packages")
        self.assertEqual(expected, actual)

    def test_reading_customfeeds(self):
        expected = ["src/gz innovationgarage https://openwrt.innovationgarage.no/packages/arm_cortex-a7_neon-vfpv4/packages/"]
        actual = self.pm.load_local_feeds_list("./configs/customfeeds")

        print(actual, "\n", expected)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
