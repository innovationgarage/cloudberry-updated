#!/usr/bin/env python3

import argparse


def run():
    parser = argparse.ArgumentParser(
        description="""
        updated is a user space daemon responsible for installing packages and 
        updating them on a OpenWrt/LEDE deployment.
        Running with no arguments is the same as '--action start'.
        """)
    parser.add_argument('--action', help='{ start | stop | restart } the daemon', default='start')
    # TODO: make pid path configurable
    return parser.parse_args()
