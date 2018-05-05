#!/usr/bin/env python3

import cli
import manager


def main(action):
    if action == "stop":
        manager.stop()
    elif action == "restart":
        manager.stop(restart=True)
        manager.start()
    else:
        manager.start()


if __name__ == '__main__':
    main(cli.run().args.action)

"""
TODO: Handle UCI file parsing from python
TODO: add init scripts in files/etc/init.d/updated {start | stop}
TODO: test on OpenWrt/LEDE install
"""
