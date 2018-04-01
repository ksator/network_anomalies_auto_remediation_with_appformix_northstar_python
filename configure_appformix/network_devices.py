from jinja2 import Template
from yaml import load

f=open('configure_appformix/network_devices.yml', 'r')
my_vars = load(f.read())
f.close()

f=open('configure_appformix/network_devices.j2')
my_template = Template(f.read())
f.close()

f=open('configure_appformix/network_devices.json','w')
f.write(my_template.render(my_vars))
f.close()
