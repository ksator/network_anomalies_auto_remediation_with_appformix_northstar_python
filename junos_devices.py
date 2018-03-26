from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import os

def collect_junos_commands(dev):
    if not os.path.exists(dev):
        os.makedirs(dev)
    device=Device (host=dev, user='lab', password='m0naco')
    device.open()
    commands = ["show version", "show chassis hardware", "show interfaces extensive"]
    for item in commands: 
        cli = device.cli(item, warning=False)
        f = open(item + '.txt', 'w')
        f.write(cli)
        f.close()
    device.close()
    return 'done'

