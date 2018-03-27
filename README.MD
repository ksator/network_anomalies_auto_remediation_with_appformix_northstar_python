[![Build Status](https://travis-ci.org/ksator/appformix_demo_scripts.svg?branch=master)](https://travis-ci.org/ksator/appformix_demo_scripts)  


## Documentation structure
[**About this repo**](README.MD#about-this-repo)  
[**Clone this repository**](README.MD#clone-this-repository)  
[**Configure Appformix to add network devices to monitor**](README.MD#configure-appformix-to-add-network-devices-to-monitor)  
[**Configure the network devices with the SNMP community used by Appformix**](README.MD#configure-the-network-devices-with-the-snmp-community-used-by-appformix)  
[**Network devices configuration for Appformix monitoring using telemetry**](README.MD#network-devices-configuration-for-appformix-monitoring-using-telemetry)  
[**webhooks**](README.MD#webhooks)  
[**Event driven automation**](README.MD#event-driven-automation)  
[**Continuous integration with Travis CI**](README.MD#continuous-integration-with-travis-ci)  
[**Looking for more automation solutions**](README.MD#looking-for-more-automation-solutions)  

## About this repo

This repository has scripts to quickly demo network devices monitoring using Appformix.  
It has also scripts to demo event driven automation leveraging Appformix.  

It has automation content to: 
- Add network devices to Appformix
- Configure the network devices with the SNMP community used by Appformix to monitor them
- Modify on the network devices the IP address configured by Appformix for telemetry
- Listen webhooks notifications sent by Appformix, and react to them (event driven automation)
- The actions triggered automatically are python scripts to:   
   - collect data on the "faulty" device and upload them on a Git server  
   - make REST calls to Northstar SDN controler to put the "faulty" device in maintenance mode. The "faulty" device will be considered
      logically down for a certain amount time, and the SDN controler will reroute the LSPs around this device during the maintenance
      period. After the maintenance period, LSPs are reverted back to optimal paths.  

I am using them with an Appformix standalone setup running version 2.15.2 installed on Ubuntu 16.04

This repository doesnt cover how to install Appformix or Northstar.  

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
apt-get install -y python-dev libxml2-dev python-pip libxslt1-dev build-essential libssl-dev libffi-dev git curl
pip install junos-eznc wget requests ipaddress cryptography flask Gitpython
```

This repository requires Northstar version 4 or above. 

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
If Appformix has serveral ip addresses, and you want to configure the network devices to use a different IP address than the one configured by appformix for telemetry server, execute the python script [**telemetry.py**](telemetry.py). 
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

## webhooks

### what is it?

A webhook is notification using an HTTP POST. A webhook is send by a system A to push data (json body as example) to a system B when an event occured in the system A. Then the system B will decide what to do with these details. Usage is event driven automation.   

### Appformix webhooks

Appformix supports webhooks. A notification is generated when the condition of an alarm is observed. You can configure an alarm to post notifications to an external HTTP endpoint. AppFormix will post a JSON payload to the endpoint for each notification.  

## Event driven automation

The script [**webhook_listener.py**](webhook_listener.py) listens to webhooks and binds a function to each URL.   
- It binds the webhook http://x.x.x.x:12345/northstar/put_device_in_maintenance (POST with JSON Body) sent by appformix to the script [**northstar_rest_calls.py**](northstar_rest_calls.py). The script [**webhook_listener.py**](webhook_listener.py) extracts the device name from the JSON body and pass it to the script [**northstar_rest_calls.py**](northstar_rest_calls.py). The script [**northstar_rest_calls.py**](northstar_rest_calls.py) then makes rest calls to Northstar SDN controler to put this device in maintenance mode. During a maintenance event, the selected devices are considered logically down, and the system reroutes the LSPs around those devices during the maintenance period. After the maintenance event is completed, delegated and PCE-initiated LSPs are reverted back to optimal paths.  
- It binds the webhook http://x.x.x.x:12345/junos/collect_data (POST with JSON body) from appformix to the script [**push_to_git.py**](push_to_git.py). The script [**webhook_listener.py**](webhook_listener.py) extracts the device name from the JSON body and pass it to the script [**push_to_git.py**](push_to_git.py). the script [**push_to_git.py**](push_to_git.py) then collects data on this junos devices (junos show commands output) and upload the data collected to a Git server.  

You first need to define webhooks on Appformix.  
From the GUI, select: settings, notification settings, notification services, add service (provide a service name and a service endpoint), setup.  

Then you can create Appformix alarms, and map these alarms to webhooks.    
You can do it from the Appformix GUI. Select add rule. Then it should be obvious. scope: select network devices, generate: select generate alert, notification: select custom service, services: select the service name you created (webhook), then save.

Then start the listener [**webhook_listener.py**](webhook_listener.py):
```
# python webhook_listener.py
 * Running on http://0.0.0.0:12345/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 290-737-301
```
Have Appformix to generate a notification (webhook).  
The python script [**webhook_listener.py**](webhook_listener.py) will receive the HTTP POST and bind it to another python functions.  

### Example with the webhook http://x.x.x.x:12345/junos/collect_data
The script [**webhook_listener.py**](webhook_listener.py) binds it to the script [**push_to_git.py**](push_to_git.py).  
The script [**webhook_listener.py**](webhook_listener.py) also extracts the device name from the JSON body and pass it to the script [**push_to_git.py**](push_to_git.py).  
Here's the output of [**webhook_listener.py**](webhook_listener.py) for the webhook http://x.x.x.x:12345/junos/collect_data  
```
172.18.0.5 - - [27/Mar/2018 13:11:30] "POST /junos/collect_data HTTP/1.1" 201 -
```
the script [**push_to_git.py**](push_to_git.py) runs on this device (the one notified by Appformix) junos show commands, collects the output, and push it to a Git server.   
The data is collected and saved the local repository (local copy of the remote repository):  
```
# ls vmx104/
show chassis hardware.txt  show interfaces extensive.txt  show version.txt
```
And then pushed on the remote repository:  
```
# git log -1
commit 38f0162a8d45419a3390d0805e43d7fe6dad4aa4
Author: ksator <ksator@juniper.net>
Date:   Tue Mar 27 13:11:16 2018 -0700

    from Gitpython
```
So the data collected is available on the remote repository:  
[**vmx104**](vmx104)  

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
