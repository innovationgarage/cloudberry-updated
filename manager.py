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


# TODO: handle stale pid


class Manager:
    def __init__(self, config_path: str) -> None:
        super().__init__()
        # Try loading the configuration file
        self.config = Configuration.load(config_path)
        if not self.config or not self.config.isValid():
            # Use the default values
            self.config = Configuration.useDefault(config_path)

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

    def start(self):
        """
        Start the main event loop.
        :return:
        """

        self.setup()
        self.main_event_loop()

    def main_event_loop(self):
        while True:
            sys.stdout.flush()
            util.log("{}: :)".format(datetime.datetime.now()))
            time.sleep(self.config.update_interval * 60)
            # TODO: check for package changes.
            # TODO: Install missing ones.
            # TODO: What todo when there is a version mismatch?
            # TODO: check OpenWisp feed file and if does not match /etc/opkg/customfeeds.conf
            package_manager.update(stdout=sys.stdout)

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
