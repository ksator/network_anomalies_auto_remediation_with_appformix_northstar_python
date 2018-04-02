from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import os
from yaml import load
import json 
from pprint import pprint 

#def get_management_ip(dev):
#    f = open(configure_appformix/network_device.json, 'r')
#    data = json.loads(f.read())
#    f.close()
#    for i in data['NetworkDeviceList']:
#        if i['NetworkDevice']['Name'] == dev:
#            management_ip = i['NetworkDevice']['ManagementIp']
#    return dev_ip

def collect_junos_commands(dev):
    if not os.path.exists('data_collected/' + dev):
        os.makedirs('data_collected/' + dev)
    f=open('configure_appformix/network_devices.yml', 'r')
    my_vars = load(f.read())
    f.close()
    if my_vars['use_snmp_2c']:
       for item in my_vars['snmp_2c']['devices']:
          if item['name'] == dev:
             dev_ip =  item['ip']
    if my_vars['use_jti']:
       for item in my_vars['jti']['devices']:
          if item['name'] == dev:
             dev_ip =  item['out_of_band']
    device=Device (host=dev_ip, user='northstar', password='Embe1mpls')
    device.open()
    commands = ["show version", "show chassis hardware", "show interfaces extensive"]
    for item in commands:
        cli = device.cli(item, warning=False)
        f = open('data_collected/' + dev +'/'+ item + '.txt', 'w')
        f.write(cli)
        f.close()
    device.close()
    return 'done'

# collect_junos_commands('jedi-vmx-1-vcp')

