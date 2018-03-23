[![Build Status](https://travis-ci.org/ksator/appformix_demo_scripts.svg?branch=master)](https://travis-ci.org/ksator/appformix_demo_scripts)  

## About this repo

This repository has scripts for Appformix with network devices monitoring.  
I am using them with an Appformix standalone setup running version 2.15.2 installed on Ubuntu 16.04

## Clone this repository

Run these commands to clone this repository:
```
sudo -s
git clone https://github.com/ksator/appformix_demo_scripts.git 
```

## Requirements to use this repository 

Run these commands to install the python library junos-eznc (also know as PyEZ) and its dependencies.
```
sudo -s
apt-get update
apt-get upgrade
apt-get install -y python-dev libxml2-dev python-pip libxslt1-dev build-essential libssl-dev libffi-dev git
pip install junos-eznc wget requests ipaddress cryptography 
```

## Configure Appformix to add network devices to monitor

Appformix supports network devices monitoring using SNMP and JTI (Juniper Telemetry Interface) streaming telemetry.  
- For SNMP, the polling interval is 60s.  
- For JTI streaming telemetry, Appformix automatically configures the network devices. The interval configured on network devices is 60s.  

Here's the [**documentation**](https://www.juniper.net/documentation/en_US/appformix/topics/concept/appformix-ansible-configure-network-device.html)  

In order to configure AppFormix for network devices monitoring, here are the steps:
- manage the 'network devices json configuration' file. This file is used to define the list of devices you want to monitor using Appformix, and the details you want to collect from them.    
- Indicate to the 'Appformix installation Ansible playbook' which 'network devices json configuration file' to use. This is done by setting the variable ```network_device_file_name``` in ```group_vars/all```
- Set the flag to enable appformix network device monitor. This is done by setting the variable ```appformix_network_device_monitoring_enabled``` to ```true``` in ```group_vars/all```
- Enable the Appformix plugins for network devices monitoring. This is done by setting the variable ```appformix_plugins``` in ```group_vars/all```
- re run the 'Appformix installation Ansible playbook'.

Here's how to manage the 'network devices json configuration file' with automation:  
Define the list of devices you want to monitor using Appformix, and the details you want to collect from them:    
```
cd appformix_demo_scripts
vi devices.yml
```

Execute the python script [**render_devices.py**](render_devices.py). It renders the template [**devices.j2**](devices.j2) using the variables [**devices.yml**](devices.yml). The rendered file is [**network_devices.json**](network_devices.json).  
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
## Configure the network devices with the SNMP community used by Appformix

You need to configure the network devices with the SNMP commninity used by Appformix. The script [**configure_snmp.py**](configure_snmp.py) renders the template [**snmp.j2**](snmp.j2) using the variables [**devices.yml**](devices.yml). The rendered file is [**snmp.conf**](snmp.conf). This file is then loaded and commited on all network devices used with SNMP monitoring.
 
```
python configure_snmp.py
configured device 172.30.52.85 with snmp community public
configured device 172.30.52.86 with snmp community public
```
```
more snmp.conf
```

## Network devices configuration for Appformix monitoring using telemetry

For JTI streaming telemetry, Appformix uses NETCONF to automatically configure the network devices:  
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
If Appformix has serveral ip addresses, and you want to configure the network devices to use another IP address for telemetry server than the one configured by appformix, execute the python script [**telemetry.py**](telemetry.py). 
The python script [**telemetry.py**](telemetry.py) renders the template [**telemetry.j2**](snmp.j2) using the variables [**devices.yml**](devices.yml). The rendered file is [**telemetry.conf**](telemetry.conf). This file is then loaded and commited on all network devices used with JTI telemetry.  

```
cd appformix_demo_scripts
vi devices.yml
```
```
python telemetry.py
configured device 172.30.52.155 with telemetry server ip 192.168.1.100
configured device 172.30.52.156 with telemetry server ip 192.168.1.100
```
```
# more telemetry.conf
set services analytics streaming-server appformix-telemetry remote-address 192.168.1.100
```
Verify on your network devices: 
```
lab@jedi-vmx-1-vcp> show configuration services analytics streaming-server appformix-telemetry remote-address
remote-address 192.168.1.100;

lab@jedi-vmx-1-vcp> show configuration | compare rollback 1
[edit services analytics streaming-server appformix-telemetry]
-    remote-address 172.30.52.157;
+    remote-address 192.168.1.100;

lab@jedi-vmx-1-vcp> show system commit
0   2018-03-23 00:34:47 UTC by lab via netconf

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
