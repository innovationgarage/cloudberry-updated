#!/usr/bin/env python3

"""
The internal configuration for the daemon is vanilla JSON.
"""
import errno
import json
import os
from collections import OrderedDict

import netjsonconfig

import util
import version
import package_manager


class Configuration:
    def __init__(self, conf=None, update_interval=10, working_directory="/var/lib/updated",
                 log_file="/var/log/updated.log", pid_file="/var/run/updated.pid") -> None:
        if conf:
            try:
                c = json.loads(conf)
                self.update_interval = int(c['update_interval'])
                self.working_directory = c['working_directory']
                self.log_file = c['log_file']
                self.pid_file = c['pid_file']
                self.version = c['version']
                self.package_manager_path = c['package_manager_path']
                # TODO: compare internal version
            except Exception as e:
                util.log("Failed to load configuration\n{}".format(e))
                self.update_interval = None
                self.working_directory = None
                self.log_file = None
                self.pid_file = None
                self.version = None
                self.package_manager_path = None
                return
        else:
            self.update_interval = update_interval
            self.working_directory = working_directory
            self.log_file = log_file
            self.pid_file = pid_file
            self.version = version.CURRENT
            self.package_manager_path = "/bin/opkg"

        # Check that a minimum value is set or default to 1
        if self.update_interval < 0.1:
            util.log("Interval value {} is too low setting it to 1\n".format(self.update_interval))
            self.update_interval = 1

    @classmethod
    def load(cls, config_path):
        """
        Load configuration file from path
        :param config_path:
        :return:
        """
        if not os.path.exists(config_path):
            return None

        config_file = open(config_path, "r").read()
        return Configuration(config_file)

    def isValid(self) -> bool:
        if self.update_interval is None or \
                self.working_directory is None or \
                self.log_file is None or \
                self.pid_file is None or \
                self.version is None or \
                self.package_manager_path is None:
            return False

        return True

    @classmethod
    def useDefault(cls, config_path: str):
        """
        Use the default values but also save the configuration for the user to make changes.
        :return:

        """
        try:
            util.create_working_directory("/var/lib/updated")
            c = Configuration()
            with open(config_path, 'w') as outfile:
                json.dump(c.to_json(), outfile)
            return c
        except PermissionError as e:
            util.log("Could not open configuration file.\nReason: {}".format(e))
            exit(errno.EPERM)

    def to_json(self):
        return dict(
            update_interval=self.update_interval,
            working_directory=self.working_directory,
            log_file=self.log_file,
            pid_file=self.pid_file,
            version=self.version,
            package_manager_path=self.package_manager_path
        )

    @classmethod
    def useUCI(cls, config_path: str):
        """
        Try using UCI configuration format.
        :return:

        """
        c = Configuration()
        config_file = open(config_path, 'r').read()
        parser = netjsonconfig.OpenWrt.parser(config=config_file)
        data = parser.parse_text(config=config_file)
        key = list(data.keys())[0]
        v = data[key][0]

        c.update_interval = v['update_interval']
        c.working_directory = v['working_directory']
        c.log_file = v['log_file']
        c.pid_file = v['pid_file']

        return c
