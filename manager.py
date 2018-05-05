#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com
import datetime
import os
import signal
import time

import lockfile

import constants
from update_daemon import UpdateDaemon


def stop(restart=False):
    """
    Terminate the currently running daemon.

    :param restart: decide whether to terminate immediately or returning to the
    call site. This is useful for starting and then stopping the daemon in the case of restart.

    :return: void
    """
    path = constants.pidfile_path()
    if os.path.exists(path + ".lock") \
            or os.path.exists(path):
        pid = int(open(constants.pidfile_path(), "r").read())
        os.kill(pid, signal.SIGTERM)
    else:
        print("No PID file found! Daemon might not be running?")

    if not restart:
        exit(0)


def setup_context():
    """
    Perform any necessary setup for the daemon.
    :return: new configured update daemon.
    """
    print("Setting up daemon")
    working_directory = constants.working_directory()
    if not os.path.exists(working_directory):
        os.mkdir(working_directory, mode=0o775)
        print("Creating working directory {}".format(working_directory))

    print("Working directory is {}".format(working_directory))

    locked_pid_file = lockfile.FileLock(constants.pidfile_path(), timeout=1)
    log_file = open(constants.log_path(), 'w+')

    context = UpdateDaemon(log_file, locked_pid_file)
    context.signal_map = {
        signal.SIGTERM: cleanup,
        signal.SIGTSTP: cleanup,
    }
    return context


def start():
    """
    Start the main event loop.
    :return:
    """
    context = setup_context()
    context.open()
    with context:
        print("Entering daemon context pid={}".format(os.getpid()))
        write_pid_file()
        while True:
            print("{}: :)".format(datetime.datetime.now()))

            # TODO: use the update interval
            time.sleep(2)


def cleanup(signum, frame):
    """
    Remove the pid file before shutting down.
    :param signum:
    :param frame:
    :return:
    """
    print("Shutting down signal={} frame={}".format(signum, frame))
    path = constants.pidfile_path()
    os.remove(path)
    exit(0)


def write_pid_file():
    """
    Store the agents pid file for later termination.
    :return:
    """
    pid_file = open(constants.pidfile_path(), "w")
    pid_file.write(str(os.getpid()))
