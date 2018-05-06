#!/usr/bin/env python3

import argparse

import version


def run():
    parser = argparse.ArgumentParser(
        description="""
        
        updated v{} is a user space daemon responsible for installing packages and 
        updating them on a OpenWrt/LEDE deployment.
        Running with no arguments is the same as '--action start'.
        """.format(version.CURRENT))
    parser.add_argument('--action', help='{ start | stop | restart } the daemon', default='start')
    parser.add_argument('--config', help='Path to the daemon configuration', default='/var/lib/updated/defaults')
    # TODO: make pid path configurable
    return parser.parse_args()
