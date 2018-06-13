#!/usr/bin/env python3

import unittest
from collections import OrderedDict

from config import Configuration


class TestPackageMangerMethods(unittest.TestCase):

    def test_read_uci(self):
        # Test valid configuration
        c = Configuration.useUCI('./configs/example_updated_config_no_comment.uci')
        self.assertEqual("10", c.update_interval)
        self.assertEqual("/etc/updated", c.working_directory)
        self.assertEqual("/var/log/updated.log", c.log_file)
        self.assertEqual("/var/run/updated.pid", c.pid_file)
        self.assertEqual("0.0.1", c.version)

        # Test valid configuration with comment
        c = Configuration.useUCI('./configs/example_updated_config.uci')
        self.assertEqual("10", c.update_interval)
        self.assertEqual("/etc/updated", c.working_directory)
        self.assertEqual("/var/log/updated.log", c.log_file)
        self.assertEqual("/var/run/updated.pid", c.pid_file)
        self.assertEqual("0.0.1", c.version)

        # TODO: test empty config
        # TODO: Test invalid configuration


if __name__ == '__main__':
    unittest.main()
