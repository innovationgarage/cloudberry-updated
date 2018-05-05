#!/usr/bin/env python3
# Copyright 2018 Alexander Alemayhu https://alemayhu.com

from daemon import daemon

import constants


class UpdateDaemon(daemon.DaemonContext):

    def __init__(self, log_file, pid_file):
        super().__init__(working_directory=constants.working_directory(),
                         pidfile=pid_file,
                         stdout=log_file)
