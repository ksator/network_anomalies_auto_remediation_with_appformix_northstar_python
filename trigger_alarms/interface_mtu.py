from jnpr.junos import Device
from lxml import etree
from yaml import load
from jnpr.junos.utils.config import Config
import time 

f=open('configure_appformix/network_devices.yml', 'r')
my_vars = load(f.read())
f.close()

dev=Device(host="192.168.128.194", user=my_vars['jti']['username'], password=my_vars['jti']['password'])
dev.open(gather_facts=False)

conf = '''
set interfaces ge-0/0/1 mtu 1000
'''
cfg=Config(dev)
cfg.lock()
cfg.load(conf, format='set')
cfg.pdiff() 
cfg.commit(comment="configured from pyez")

print 'wait 70 seconds'
time.sleep(70)

cfg.rollback(1)
cfg.pdiff() 
cfg.commit(comment="rollbacked from pyez")

cfg.unlock()
dev.close()

