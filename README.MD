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

Appformix supports network devices monitoring using SNMP and JTI telemetry.  
- For SNMP, the polling interval is 60s.  
- For JTI streaming telemetry, Appformix automatically configures the network devices, with an interval of 60s.  

Define the list of devices you want to monitor using Appformix:  
```
vi devices.yml
```
The script [**render_devices.py**](render_devices.py) renders the template [**devices.j2**](devices.j2) using the variables [**devices.yml**](devices.yml). The rendered file is [**network_devices.json**](network_devices.json).  
```
python render_devices.py
more network_devices.json
```

 
