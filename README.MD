[![Build Status](https://travis-ci.org/ksator/appformix_demo_scripts.svg?branch=master)](https://travis-ci.org/ksator/appformix_demo_scripts)  

## About this repo

This repository has scripts for Appformix.  
This has been tested with an Appformix standalone setup running version 2.15.2 

## How to clone this repository

From your appformix server, run these commands on your laptop:
```
sudo -s
git clone https://github.com/ksator/appformix_demo_scripts.git 
```

## Configure an SNMP community on network devices
For Appformix to monitor network devices using SNMP, configure the SNMP community used by Appformix on the network devices:  
```
set snmp community public
commit and-quit
```


## Configure Appformix for network devices monitoring

Appformix supports network devices monitoring using SNMP and JTI (Juniper Telemetry Interface) streaming telemetry.  
- For SNMP, the polling interval is 60s.  
- For JTI streaming telemetry, Appformix automatically configures the network devices. The interval configured on network devices is 60s.  

Here's the [**documentation**](https://www.juniper.net/documentation/en_US/appformix/topics/concept/appformix-ansible-configure-network-device.html)  

In order to configure AppFormix for network devices monitoring, here are the steps:
- manage the 'network devices json configuration' file.  
  This file is used to define the list of devices you want to monitor using Appformix, and the details you want to collect from them.    
- Indicate to the 'Appformix installation Ansible playbook' which 'network devices json configuration file' to use.  
  This is done by setting the variable ```network_device_file_name``` in ```group_vars/all```
- Set the flag to enable appformix network device monitor.  
  This is done by setting the variable ```appformix_network_device_monitoring_enabled``` to ```true``` in ```group_vars/all```
- Enable the Appformix plugins for network devices monitoring.  
  This is done by setting the variable ```appformix_plugins``` in ```group_vars/all```
- re run the 'Appformix installation Ansible playbook'.

Here's how to manage the 'network devices json configuration file' with automation:  
Define the list of devices you want to monitor using Appformix, and the details you want to collect from them:    
```
cd appformix_demo_scripts
ls
vi devices.yml
```
The script [**render_devices.py**](render_devices.py) renders the template [**devices.j2**](devices.j2) using the variables [**devices.yml**](devices.yml). The rendered file is [**network_devices.json**](network_devices.json).  
```
python render_devices.py
more network_devices.json
```

From your appformix directory, update ```group_vars/all``` file: 
```
cd appformix-2.15.2/
vi group_vars/all
```
to make sure it contains this:
```
network_device_file_name: /path_to_appformix_demo_scripts_directory/network_devices.json
appformix_network_device_monitoring_enabled: true
appformix_jti_network_device_monitoring_enabled: true
appformix_plugins:
   - plugin_info: 'certified_plugins/jti_network_device_usage.json'
   - plugin_info: 'certified_plugins/snmp_network_device_routing_engine.json'
   - plugin_info: 'certified_plugins/snmp_network_device_usage.json'
```

Then, from your appformix directory, re-run the 'Appformix installation Ansible playbook':
```
cd appformix-2.15.2/
ansible-playbook -i inventory appformix_standalone.yml
```

for JTI monitoring, Appformix should configures the network devices using NETCONF 
```
lab@jedi-vmx-1-vcp> show system commit
0   2018-03-22 16:32:37 UTC by lab via netconf
1   2018-03-22 16:32:33 UTC by lab via netconf
```
```
lab@jedi-vmx-1-vcp> show configuration | compare rollback 1
[edit services analytics]
+    sensor Interface_Sensor {
+        server-name appformix-telemetry;
+        export-name appformix;
+        resource /junos/system/linecard/interface/;
+    }

lab@jedi-vmx-1-vcp> show configuration | compare rollback 2
[edit]
+  services {
+      analytics {
+          streaming-server appformix-telemetry {
+              remote-address 172.30.52.157;
+              remote-port 42596;
+          }
+          export-profile appformix {
+              local-address 192.168.1.1;
+              local-port 21112;
+              dscp 20;
+              reporting-rate 60;
+              format gpb;
+              transport udp;
+          }
+          sensor Interface_Sensor {
+              server-name appformix-telemetry;
+              export-name appformix;
+              resource /junos/system/linecard/interface/;
+          }
+      }
+  }

lab@jedi-vmx-1-vcp>

```
in case appformix has serveral ip addresses, make sure the junos devices are configured with the one you want to use: 
```
[edit]
lab@jedi-vmx-1-vcp# show services analytics | display set
set services analytics streaming-server appformix-telemetry remote-address 172.30.52.157
set services analytics streaming-server appformix-telemetry remote-port 42596
set services analytics export-profile appformix local-address 192.168.1.1
set services analytics export-profile appformix local-port 21112
set services analytics export-profile appformix dscp 20
set services analytics export-profile appformix reporting-rate 60
set services analytics export-profile appformix format gpb
set services analytics export-profile appformix transport udp
set services analytics sensor Interface_Sensor server-name appformix-telemetry
set services analytics sensor Interface_Sensor export-name appformix
set services analytics sensor Interface_Sensor resource /junos/system/linecard/interface/

[edit]
lab@jedi-vmx-1-vcp# set services analytics streaming-server appformix-telemetry remote-address 192.168.1.100

[edit]
lab@jedi-vmx-1-vcp# show | compare
[edit services analytics streaming-server appformix-telemetry]
-    remote-address 172.30.52.157;
+    remote-address 192.168.1.100;

[edit]
lab@jedi-vmx-1-vcp# commit and-quit
commit complete
Exiting configuration mode

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
