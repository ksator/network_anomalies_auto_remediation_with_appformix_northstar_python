from jnpr.junos.utils.config import Config
import os
from yaml import load

def collect_junos_commands(dev):
    if not os.path.exists(dev):
        os.makedirs(dev)
    f=open('devices.yml', 'r')
    my_vars = load(f.read())
    f.close()
    if use_snmp_2c == True
       for item in my_vars['snmp_2c']['devices']:
          if item['name'] == dev:
             dev_ip =  item['ip']
    if use_jti == True
       for item in my_vars['jti']['devices']:
          if item['name'] == dev:
             dev_ip =  item['out_of_band']
    device=Device (host=dev_ip, user='northstar', password='Embe1mpls')
    device.open()
    commands = ["show version", "show chassis hardware", "show interfaces extensive"]
    for item in commands:
        cli = device.cli(item, warning=False)
        f = open(dev +'/'+ item + '.txt', 'w')
        f.write(cli)
        f.close()
    device.close()
    return 'done'
