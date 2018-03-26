import git
import os
from junos import collect_junos_commands

dev='172.30.52.152'

cwd = os.getcwd()
repo = git.Repo(cwd)
# print repo.git.status()

repo.git.pull()

collect_junos_commands(dev)

# f=open(cwd + '/test.md', 'w')
# f.write("blabla")
# f.close()

# print repo.git.status()
# print repo.git.add("test.md")
# repo.git.add("test.md")
print repo.git.add(".")

# print repo.git.status()
# print repo.git.commit(m = "from Gitpython")
repo.git.commit(m = "from Gitpython")
# print repo.git.status()
# print repo.git.push()
repo.git.push()

