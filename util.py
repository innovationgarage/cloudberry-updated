#!/usr/bin/env python3
import datetime
import os


# This function is needed both by config and manager. Moving it here to avoid a circular dependency that breaks test
# runs
def create_working_directory(pwd: str):
    if not os.path.exists(pwd):
        os.mkdir(pwd, mode=0o775)
        log("Creating working directory {}".format(pwd))


def log(msg):
    print(datetime.datetime.now(), end=': ')
    print(msg)
