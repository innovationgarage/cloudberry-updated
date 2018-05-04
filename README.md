# updated

updated is a user space daemon responsible for installing packages and updating
them. The project uses UCI for all configuration and the actual package
management is done by opkg.

updated can be considered as a sort of duck tape to make OpenWisp2
configuration let you handle the packages to be installed on a device via the
same UI.

## Design

TODO: ...


## Example configuration

    config daemon 'daemon'
        option update_interval '10m'
    config package_name 'package_name''
        option version 'x.y'
