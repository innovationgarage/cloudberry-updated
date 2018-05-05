#!/usr/bin/env python3

package_manager_path = "/bin/opkg"


class PackageManager:

    @staticmethod
    def dry_run(prefix: str, packages: []):
        """
       Return a valid command
       :param prefix:
       :param packages:
       :return:
       """
        if not packages and len(packages) == 0:
            if prefix == "update":
                return "{} update".format(package_manager_path)
            return ""

        command = "{} {}".format(package_manager_path, prefix)
        for p in packages:
            command += " {}".format(p)
        return command
