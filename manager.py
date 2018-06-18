#!/usr/bin/env python3
import datetime
import errno
import os
import signal
import sys
import time

import package_manager
import util
from config import Configuration


class Manager:
    our_packages = {}
    cached_packages_timestamp = None
    packages_path = "/etc/updated/packages"

    def __init__(self, config_path: str) -> None:
        super().__init__()
        self.config = Configuration.load(config_path)
        if not self.config:
            util.log("Error found no configuration")
            exit(1)
        self.pm = package_manager.PackageManager(self.config.package_manager_path)
        if not self.config or not self.config.isValid():
            util.log("Error invalid configuration")
            exit(1)

    def stop(self, restart=False):
        """
        Terminate the currently running daemon.
    
        :param restart: decide whether to terminate immediately or returning to the
        call site. This is useful for starting and then stopping the daemon in the case of restart.
    
        :return: void
        """
        path = self.config.pid_file
        if os.path.exists(path + ".lock") \
                or os.path.exists(path):
            pid = int(open(path, "r").read())

            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError as e:
                util.log("Failed to kill running daemon.\nReason: {}".format(e))
        else:
            util.log("No PID file found! Daemon might not be running?")

        if not restart:
            exit(0)

    def setup(self):
        """
        Perform any necessary setup for the daemon.
        :return: new configured update daemon.
        """
        util.create_working_directory(self.config.working_directory)
        self.packages_path = os.path.join(self.config.working_directory, "packages")
        try:
            sys.stdout = open(self.config.log_file, 'w+')
            util.log("Setting up daemon")
            os.chdir(self.config.working_directory)
            signal.signal(signal.SIGTERM, self.cleanup)
            signal.signal(signal.SIGTSTP, self.cleanup)
        except PermissionError as e:
            util.log("Could not open log file file://{}\n{}".format(self.config.log_file, e))
            self.remove_pid_file()
            exit(errno.EPERM)
        self.write_pid_file()
        self.pm.load_local_packages_list(self.packages_path)

    def start(self):
        """
        Start the main event loop.
        :return:
        """

        self.setup()
        self.main_event_loop()

    def main_event_loop(self):
        util.log("Entering main event loop")
        while True:
            sys.stdout.flush()
            util.log("{}: :)".format(datetime.datetime.now()))
            time.sleep(self.config.update_interval * 1)

            self.load_local_packages_list()

            installed_packages = self.pm.run_list_installed(stdout=sys.stdout)
            if len(installed_packages) != 0:
                for key in self.our_packages:
                    util.log("Checking for {} in installed list".format(key))
                    if key not in installed_packages:
                        self.pm.update(stdout=sys.stdout)
                        exit_code = self.pm.run_install(packages=[key], stdout=sys.stdout)
                        if exit_code != 0:
                            util.log("Error: Got bad exit({}) while installing {}".format(exit_code, key))

            # TODO: check for package changes.
            # TODO: What todo when there is a version mismatch?
            # TODO: check OpenWisp feed file and if does not match /etc/opkg/customfeeds.conf

    def cleanup(self, signum, frame):
        """
        Remove the pid file before shutting down.
        :param signum:
        :param frame:
        :return:
        """
        util.log("Shutting down signal={} frame={}".format(signum, frame))
        self.remove_pid_file()
        exit(0)

    def remove_pid_file(self):
        path = self.config.pid_file
        os.remove(path)

    def write_pid_file(self):
        """
        Store the agents pid file for later termination.
        :return:
        """
        pid_file = open(self.config.pid_file, "w")
        pid_file.write(str(os.getpid()))

    def load_local_packages_list(self):
        """
        Poll the filesystem to detect changes to the packages file.
        :return:
        """
        stamp = os.stat(self.packages_path).st_mtime
        if stamp != self.cached_packages_timestamp:
            print("Reloading packages from filesystem")
            self.cached_packages_timestamp = stamp
            self.our_packages = self.pm.load_local_packages_list(self.packages_path)
