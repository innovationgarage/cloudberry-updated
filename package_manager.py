#!/usr/bin/env python3
import subprocess

"""
A small wrapper around opkg.
"""


class PackageManager:

    def __init__(self, path: str) -> None:
        super().__init__()
        self.package_manager_path = path

    def dry_run(self, prefix: str, packages: []):
        """
       Return a valid command
        :param package_manager_path:
       :param prefix:
       :param packages:
       :return:
       """
        if not packages and len(packages) == 0:
            if prefix == "update" or prefix == "upgrade":
                return "{} {}".format(self.package_manager_path, prefix)
            return ""

        command = "{} {}".format(self.package_manager_path, prefix)
        for p in packages:
            command += " {}".format(p)
        return command

    def update(self, stdout):
        """
        Update the list of packages:
        :param stdout:
        :return:
        """
        prompt = self.dry_run("update", [])
        p = subprocess.Popen(prompt.split(" "), stdout=stdout, stderr=stdout)
        p.wait()  # TODO: use timeout?
