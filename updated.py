#!/usr/bin/env python3

import cli
import manager


def main(args):
    action = args.action
    m = manager.Manager(args.config)
    if action == "stop":
        m.stop()
    elif action == "restart":
        m.stop(restart=True)
        m.start()
    else:
        m.start()


if __name__ == '__main__':
    main(cli.run().args)

"""
TODO: Handle UCI file parsing from python
TODO: add init scripts in files/etc/init.d/updated {start | stop}
TODO: test on OpenWrt/LEDE install
"""
