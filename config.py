#!/usr/bin/env python3

"""
The internal configuration for the daemon is vanilla JSON.
"""
import json
import os


class Configuration:
    def __init__(self, conf=None, update_interval=10, working_directory ="/var/lib/updated",
                 log_file="/var/log/updated.log", pid_file="/var/run/updated.pid") -> None:
        try:
            c = json.loads(conf)
        except Exception as e:
            print("Failed to load configuration\n{}".format(e))
            self.update_interval = None
            self.working_directory = None
            self.log_file = None
            self.pid_file = None
        else:
            # Handle user passing in bad values
            try:
                self.update_interval = float(c['daemon']['update_interval'])
                self.working_directory = c['daemon']['working_directory']
                self.log_file = c['daemon']['log_file']
                self.pid_file = c['daemon']['pid_file']
            except Exception as et:
                print("Failed to use this configuration -> {}\nReason: {}".format(c, et))
                self.update_interval = update_interval
                self.working_directory = working_directory
                self.log_file = log_file
                self.pid_file = pid_file
                print("Falling back to -> {}".format(self.to_json()))
            else:
                # Check that a minimum value is set or default to 1
                if self.update_interval < 0.1:
                    print("Interval value {} is too low setting it to 1\n".format(self.update_interval))
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
