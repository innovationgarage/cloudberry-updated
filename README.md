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
        option update_interval '10'
        option working_directory '/var/lib/updated'
        option log_file '/var/log/updated.log'
        option pid_file '/var/run/updated.pid'
    config package_name 'package_name'
        option version 'x.y'
  
  TODO: explain above configuration 

### Usage


    # Start the daemon
    ./updated

    # Stop the daemon
    ./updated --action stop

    # Restart the daemon
    ./updated --action restart

