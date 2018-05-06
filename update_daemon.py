#!/usr/bin/env python3

from daemon import daemon


class UpdateDaemon(daemon.DaemonContext):

    def __init__(self, log_file, pid_file, working_directory):
        super().__init__(working_directory=working_directory,
                         pidfile=pid_file,
                         stdout=log_file)
