from jnpr.junos import Device
from jnpr.junos.utils.config import Config

def collect_junos_commands(dev):
    device=Device (host=dev, user='lab', password='m0naco')
    device.open()
    commands = ["show version", "show chassis hardware", "show interface ge-0/0/o extensive"]
    for item in commands: 
        cli = device.cli(item, warning=False)
        f = open(item + '.txt', 'w')
        f.write(cli)
        f.close()
    device.close()
    return 'done'

