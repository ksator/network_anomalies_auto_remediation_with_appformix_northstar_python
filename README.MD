[![Build Status](https://travis-ci.org/ksator/appformix_demo_scripts.svg?branch=master)](https://travis-ci.org/ksator/appformix_demo_scripts)  

## About this repo

This repository has scripts for Appformix

## How to clone this repository

Run these commands on your laptop:
```
sudo -s
git clone https://github.com/ksator/appformix_demo_scripts.git 
cd appformix_demo_scripts
```

## Configure Appformix for network devices monitoring

Appformix supports network devices monitoring using SNMP and JTI (Juniper Telemetry Interface) streaming telemetry.  
- For SNMP, the polling interval is 60s.  
- For JTI streaming telemetry, Appformix automatically configures the network devices. The interval configured on network devices is 60s.  

Here's the [**documentation**](https://www.juniper.net/documentation/en_US/appformix/topics/concept/appformix-ansible-configure-network-device.html)  

In order to configure AppFormix for network devices monitoring, here are the steps:
- manage the network devices json configuration file. 
  This file is used to define the list of devices you want to monitor using Appformix, and the details you want to collect from them.    
- Indicate to the Appformix installation Ansible playbook which network devices json configuration file to use. 
  This is done by setting the variable ```network_device_file_name``` in ```group_vars/all``` 
- Enable the Appformix plugins for network devices monitoring. 
  This is done by setting the variable ```appformix_plugins``` in ```group_vars/all```.
- re run the Appformix installation Ansible playbook.

Here's how to manage network devices json configuration file with automation:  

Define the list of devices you want to monitor using Appformix, and the details you want to collect from them:    
```
vi devices.yml
```
The script [**render_devices.py**](render_devices.py) renders the template [**devices.j2**](devices.j2) using the variables [**devices.yml**](devices.yml). The rendered file is [**network_devices.json**](network_devices.json).  
```
python render_devices.py
more network_devices.json
```

## Continuous integration with Travis CI

There is a github webhook with Travis CI  
The syntax of the python scripts in this repository are tested automatically by Travis CI.  
The files [**.travis.yml**](.travis.yml) and [**requirements.txt**](requirements.txt) at the root of this repository are used for this.  

Here's the last build status
[![Build Status](https://travis-ci.org/ksator/appformix_demo_scripts.svg?branch=master)](https://travis-ci.org/ksator/appformix_demo_scripts)

## Looking for more automation solutions

https://github.com/ksator?tab=repositories  
https://gitlab.com/users/ksator/projects  
https://gist.github.com/ksator/  
