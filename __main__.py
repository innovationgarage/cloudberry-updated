#!/usr/bin/env python3

import cli
import daemonrunner


def main(args):
    action = args.action
    m = daemonrunner.DaemonRunner(args.config)
    try:
        if action == "stop":
            m.stop()
        elif action == "restart":
            m.stop(restart=True)
            m.start()
        else:
            m.start()
    except KeyboardInterrupt:
        m.stop()


if __name__ == '__main__':
        main(cli.run())


"""
TODO: Handle UCI file parsing from python
TODO: add init scripts in files/etc/init.d/updated {start | stop}
TODO: test on OpenWrt/LEDE install
"""
