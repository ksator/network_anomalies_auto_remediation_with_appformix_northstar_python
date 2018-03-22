[![Build Status](https://travis-ci.org/ksator/appformix_demo_scripts.svg?branch=master)](https://travis-ci.org/ksator/appformix_demo_scripts)  

### About this repo

This repository has scripts for Appformix

### How to clone this repository

Run these commands on your laptop:
```
sudo -s
git clone https://github.com/ksator/appformix_demo_scripts.git 
cd appformix_demo_scripts
```

### Configure Appformix for network devices monitoring

Appformix supports network devices monitoring using SNMP and JTI telemetry.  
- For SNMP, the polling interval is 60s.  
- For JTI streaming telemetry, Appformix automatically configures the network devices, with an interval of 60s.  

Here's the [**documentation**](https://www.juniper.net/documentation/en_US/appformix/topics/concept/appformix-ansible-configure-network-device.html)  

In order to configure AppFormix for network devices monitoring, we use a network devices json configuration file.  Here's how to manage this file with automation:  

Define the list of devices you want to monitor using Appformix, and the details you want to collect:    
```
vi devices.yml
```
The script [**render_devices.py**](render_devices.py) renders the template [**devices.j2**](devices.j2) using the variables [**devices.yml**](devices.yml). The rendered file is [**network_devices.json**](network_devices.json).  
```
python render_devices.py
more network_devices.json
```

### Continuous integration with Travis CI

There is a github webhook with Travis CI  
The syntax of the python scripts in this repository are tested automatically by Travis CI.  
The files [**.travis.yml**](.travis.yml) and [**requirements.txt**](requirements.txt) at the root of this repository are used for this.  

Here's the last build status
[![Build Status](https://travis-ci.org/ksator/appformix_demo_scripts.svg?branch=master)](https://travis-ci.org/ksator/appformix_demo_scripts)

### Looking for more automation solutions

https://github.com/ksator?tab=repositories  
https://gitlab.com/users/ksator/projects  
https://gist.github.com/ksator/  
