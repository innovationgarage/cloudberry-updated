#!/usr/bin/env python3

import unittest

from config import Configuration


class TestPackageMangerMethods(unittest.TestCase):

    def test_internal_repsentation(self):
        example = """
{
  "daemon": {
    "update_interval": "10",
    "working_directory": "/var/lib/updated",
    "log_file": "/var/log/updated.log",
    "pid_file": "/var/run/updated.pid"
  }
}
"""
        c = Configuration(example)
        self.assertIsNotNone(c)

        self.assertEqual(10, c.update_interval)
        self.assertEqual("/var/lib/updated", c.working_directory)
        self.assertEqual("/var/log/updated.log", c.log_file)
        self.assertEqual("/var/run/updated.pid", c.pid_file)

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
  "daemon": {
    "update_interval": "0",
    "working_directory": "/var/lib/updated",
    "log_file": "/var/log/updated.log",
    "pid_file": "/var/run/updated.pid"
  }
}
"""
        c = Configuration(zero_update_interval)
        self.assertIsNotNone(c)
        self.assertEqual(c.update_interval, 1)


    # TODO: test UCI format


if __name__ == '__main__':
    unittest.main()
