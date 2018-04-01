from jinja2 import Template
from yaml import load
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

f=open('network_devices.yml', 'r')
my_vars = load(f.read())
f.close()

f=open('snmp.j2')
my_template = Template(f.read())
f.close()

f=open('snmp.conf','w')
f.write(my_template.render(my_vars))
f.close()

for item in my_vars['snmp_2c']['devices']:
    device=Device (host=item['ip'], user=my_vars['jti']['username'], password=my_vars['jti']['password'])
    device.open()
    cfg=Config(device)
    cfg.load(path='snmp.conf', format='set')
    cfg.commit()
    device.close()
    print 'configured device ' + item['ip'] + ' with snmp community ' +  my_vars['snmp_2c']['community']



