#!/usr/bin/env python3
import subprocess

import netjsonconfig

import util

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

    def run_install(self, packages: [], stdout):
        prompt = self.dry_run("install", packages)
        p = subprocess.Popen(prompt.split(" "), stdout=stdout, stderr=stdout)
        p.communicate()
        return p.wait()

    @staticmethod
    def list_installed_to_dict(output):
        lines = output.split("\n")

        packages = {}
        for line in lines:
            if len(line.strip()) == 0:
                continue
            # Only split by first dash, version number could use a dash later
            package_info = line.split("-", 1)
            if len(package_info) < 2:
                util.log("Invalid package list, expecting format (package - version), but got ".format(package_info))
            packages[package_info[0].strip()] = package_info[1].strip()

        return packages

    def run_list_installed(self, stdout):
        prompt = "{} list-installed".format(self.package_manager_path)
        util.log("exec: {}".format(prompt))
        p = subprocess.run(prompt.split(" "), stderr=stdout, stdout=subprocess.PIPE)
        return self.list_installed_to_dict(p.stdout.decode('utf-8'))

    @staticmethod
    def load_local_packages_list(path):
        # Only get the packages from the UCI file
        config_file = open(path, 'r').read()
        parser = netjsonconfig.OpenWrt.parser(config=config_file)
        data = parser.parse_text(config=config_file)
        v = data["\'updated\'"][0]
        packages = {}
        for k in v:
            if k != ".name" and k != ".type":
                packages[k] = v[k]
        return packages
