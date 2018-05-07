#!/usr/bin/env python3

import unittest

from config import Configuration


class TestPackageMangerMethods(unittest.TestCase):

    def test_internal_repsentation(self):
        example = """
{
    "version": "0.0.1",
    "update_interval": "10",
    "working_directory": "/var/lib/updated",
    "log_file": "/var/log/updated.log",
    "pid_file": "/var/run/updated.pid",
    "package_manager_path": "/bin/opkg"
}
"""
        c = Configuration(example)
        self.assertIsNotNone(c)

        self.assertEqual(10, c.update_interval)
        self.assertEqual("/var/lib/updated", c.working_directory)
        self.assertEqual("/var/log/updated.log", c.log_file)
        self.assertEqual("/var/run/updated.pid", c.pid_file)
        self.assertEqual("0.0.1", c.version)
        self.assertEqual("/bin/opkg", c.package_manager_path)

    def test_invalid_configuration(self):
        c = Configuration("""
        { 23929323:19101:222222222222222222:111923:: }
        """)
        self.assertIsNone(c.update_interval)
        self.assertIsNone(c.working_directory)
        self.assertIsNone(c.log_file)
        self.assertIsNone(c.pid_file)

        zero_update_interval = """
{
    "version": "0.0.1",
    "update_interval": "0",
    "working_directory": "/var/lib/updated",
    "log_file": "/var/log/updated.log",
    "pid_file": "/var/run/updated.pid",
    "package_manager_path": "/bin/opkg"
}
"""
        c = Configuration(zero_update_interval)
        self.assertIsNotNone(c)
        self.assertEqual(c.update_interval, 1)

        null_fields = """
{
    "version": null,
    "update_interval": null,
    "working_directory": null,
    "log_file": null,
    "pid_file": null,
    "package_manager_path": "null"
}
"""
        c = Configuration(null_fields)
        self.assertIsNotNone(c)
        self.assertIsNone(c.update_interval)

    # TODO: test UCI format


if __name__ == '__main__':
    unittest.main()
