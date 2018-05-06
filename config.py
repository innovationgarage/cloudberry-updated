#!/usr/bin/env python3

"""
The internal configuration for the daemon is vanilla JSON.
"""
import json
import os


class Configuration:
    # Update interval in minutes
    update_interval: float = 10
    working_directory: str = "/var/lib/updated"
    log_file: str = "/var/log/updated.log"
    pid_file: str = "/var/run/updated.pid"

    def __init__(self, conf=None) -> None:
        try:
            c = json.loads(conf)
        except Exception as e:
            print("Failed to load configuration\n{}".format(e))
            self.update_interval = None
            self.working_directory = None
            self.log_file = None
            self.pid_file = None
        else:
            self.update_interval = float(c['daemon']['update_interval'])
            # Check that a minimum value is set or default to 1
            if self.update_interval < 0.1:
                self.update_interval = 1
            self.working_directory = c['daemon']['working_directory']
            self.log_file = c['daemon']['log_file']
            self.pid_file = c['daemon']['pid_file']

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
        if self.update_interval is None or\
                self.working_directory is None or\
                self.log_file is None or\
                self.pid_file is None:
            return False

        return True

    @classmethod
    def useDefault(cls, config_path: str):
        """
        Use the default values but also save the configuration for the user to make changes.
        :return:
        """
        c = Configuration()
        with open(config_path, 'w') as outfile:
            json.dump(c.to_json(), outfile)

        return c

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
