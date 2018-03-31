from jnpr.junos import Device
from lxml import etree
from yaml import load

f=open('devices.yml', 'r')
my_vars = load(f.read())
f.close()

dev=Device(host="192.168.128.194", user=my_vars['jti']['username'], password=my_vars['jti']['password'])
dev.open()
test1=dev.rpc.ping(host="10.1.0.10", rapid=True, count='10000')
#print etree.tostring(test1)
dev.close()
