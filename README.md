# updated

NOTE: This project is still under early development, so somethings are missing.

updated is a user space daemon responsible for installing packages and updating
them. The project uses UCI for all external configuration and the actual package
management is done by opkg.

updated can be considered as a sort of duck tape to make OpenWisp2 configuration
let you handle the packages to be installed on a device via the same UI.

## Design

updated receives it's configuration from `/etc/config/updated`.  The
configuration file has the following structure

    # Daemon
    package 'updated'

    config updated
        option update_interval '10'
        option working_directory '/etc/updated'
        option log_file '/var/log/updated.log'
        option pid_file '/var/run/updated.pid'
        option version '0.0.1'
        
The daemon section has all of the configuration specific for how updated is
supposed to run.  The feeds section has a list off all the custom feeds and
packages shows the packages to be installed.
  
### Usage


    # Start the daemon
    ./updated

    # Stop the daemon
    ./updated --action stop

    # Restart the daemon
    ./updated --action restart

