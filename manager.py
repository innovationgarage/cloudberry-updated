#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com
import datetime
import errno
import os
import signal
import time

import lockfile

from config import Configuration
from update_daemon import UpdateDaemon


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
            os.kill(pid, signal.SIGTERM)
        else:
            print("No PID file found! Daemon might not be running?")

        if not restart:
            exit(0)

    def setup_context(self):
        """
        Perform any necessary setup for the daemon.
        :return: new configured update daemon.
        """
        print("Setting up daemon")
        pwd = self.config.working_directory
        if not os.path.exists(pwd):
            os.mkdir(pwd, mode=0o775)
            print("Creating working directory {}".format(pwd))

        print("Working directory is {}".format(pwd))

        locked_pid_file = lockfile.FileLock(self.config.pid_file, timeout=1)

        try:
            log_file = open(self.config.log_file, 'w+')
            context = UpdateDaemon(log_file, locked_pid_file, self.config.working_directory)
            context.signal_map = {
                signal.SIGTERM: self.cleanup,
                signal.SIGTSTP: self.cleanup,
            }
            return context
        except PermissionError as e:
            print("Could not open log file file://{}\n{}", self.config.log_file, e)
            self.remove_pid_file()
            exit(errno.EPERM)

    def start(self):
        """
        Start the main event loop.
        :return:
        """

        context = self.setup_context()
        context.open()
        with context:
            print("Entering daemon context pid={}".format(os.getpid()))
            self.write_pid_file()
            while True:
                print("{}: :)".format(datetime.datetime.now()))
                time.sleep(self.config.update_interval * 60)

    def cleanup(self, signum, frame):
        """
        Remove the pid file before shutting down.
        :param signum:
        :param frame:
        :return:
        """
        print("Shutting down signal={} frame={}".format(signum, frame))
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
