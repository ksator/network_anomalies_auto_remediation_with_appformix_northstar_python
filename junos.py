from jnpr.junos import Device
from jnpr.junos.utils.config import Config

device=Device (host='172.30.52.152', user='lab', password='m0naco')
device.open()

commands = ["show version", "show chassis hardware"]

for item in commands: 
 cli = device.cli(item, warning=False)
 f = open(item + '.txt', 'w')
 f.write(cli)
 f.close()

device.close()

