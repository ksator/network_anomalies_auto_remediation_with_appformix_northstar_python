import git
import os
import junos_devices

def collect_and_push(dev):
    cwd = os.getcwd()
    repo = git.Repo(cwd)
    repo.git.pull('origin', 'master')
    junos_devices.collect_junos_commands(dev)
    print repo.git.add(dev + "/.")
    repo.git.commit(m = "from Gitpython")
    repo.git.push('origin', 'master')
    return "done"
