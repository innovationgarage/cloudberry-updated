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
    config updated
        option update_interval '10'
        option working_directory '/var/lib/updated'
        option log_file '/var/log/updated.log'
        option pid_file '/var/run/updated.pid'
        option version '0.0.1'
        
        
    # Package feeds
    config feeds 'customfeeds'
       config packages 'packages'
            option type 'src-git' 
            option location 'https://github.com/openwrt/packages.git'
       config xwrt 'xwrt'
            option type 'src-svn' 
            option location 'http://x-wrt.googlecode.com/svn/trunk/package'
       config custom 'custom' 
            option type 'src-link' 
            option location '/usr/src/openwrt/custom-feed'
    
    # Packages
    config packages 'packages'
       config bash 'bash'
            option version '3.2.57'
            option state 'installed'
       config iptables 'iptables'
            option state 'installed'

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

