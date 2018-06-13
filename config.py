#!/usr/bin/env python3

"""
The internal configuration for the daemon is vanilla JSON.
"""
import errno
import json
import os

import netjsonconfig

import util
import version


class Configuration:

    def __init__(self) -> None:
        self.version = "0.0.1"

    @classmethod
    def load(cls, config_path):
        """
        Load configuration file from path
        :param config_path:
        :return:
        """
        if not os.path.exists(config_path):
            return None

        return cls.useUCI(config_path)

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
            util.create_working_directory("/etc/updated")
            c = Configuration()
            with open(config_path, 'w') as outfile:
                json.dump(c.to_json(), outfile)
            # Check that a minimum value is set or default to 1
            if c.update_interval < 0.1:
                util.log("Interval value {} is too low setting it to 1\n".format(c.update_interval))
                c.update_interval = 1
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
        v = data["\'updated\'"][0]

        c.update_interval = int(v['update_interval'])
        c.working_directory = v['working_directory']
        c.log_file = v['log_file']
        c.pid_file = v['pid_file']

        return c
