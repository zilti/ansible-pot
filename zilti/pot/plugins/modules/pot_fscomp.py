# -*- Coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import re
import subprocess
from os.path import exists
from ansible.module_utils.basic import AnsibleModule


__metaclass__ = type


DOCUMENTATION = r"""
---
module: pot_fscomp
short_description: Pot fscomp task.
version_added: 0.1.0
description:
  - Pot fscomp task.
author: "Daniel Ziltener <dziltener@lyrion.ch>"
options:
  name:
      description:
        - The fscomp name
      type: str
      required: True
      default: None
  state:
      type: str
      required: False
      default: 'present'
      choices: [ 'present', 'absent' ]
  ignore:
      description:
        - Ignore this task?
      type: bool
      required: False
      default: False
  
requirements:
  - FreeBSD with Root-on-ZFS
"""

EXAMPLES = r"""
"""


class PotFSComp(object):
    def __init__(self, module, **kwargs):
        self.module = module
        self.params = kwargs["params"]
        self.executable = [module.get_bin_path("pot", True)]
    
    def _exec(self, args, env={}):
        res = subprocess.run(
            args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode, res.stdout.decode('utf-8'), res.stderr.decode('utf-8')
    
    def pot_root(self):
        rc, out, err = self._exec([self.executable[0], "config", "-g", "fs_root"])
        return out.split("=")[1].strip()
    
    def pot_zfs_root(self):
        rc, out, err = self._exec([self.executable[0], "config", "-g", "zfs_root"])
        return out.split("=")[1].strip()
    def fscomp_exists(self):
        return exists(self.pot_root()+'/fscomp/'+self.params["name"])
    def create(self):
        if self.params["state"] == "present" and not self.fscomp_exists():
            cmd = [self.executable[0], "create-fscomp"]
            if "name" in self.params and self.params["name"]:
                cmd.append("-f")
                cmd.append(self.params["name"])
            
            rc, out, err = self._exec(cmd)
            return True, out, err
        else:
            return False, None, None
    def destroy(self):
        if self.params["state"] == "absent" and self.fscomp_exists():
            cmd = [self.executable[0], "destroy", "-f", self.params["name"]]
            rc, out, err = self._exec(cmd)
            return True, out, err
        else:
            return False, None, None


def main():
    arg_spec = dict(
        name=dict(default=None, type="str"),
        state=dict(default='present', type="str", choices=['present', 'absent']),
        ignore=dict(default=False, type="bool"))
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    fscomp = PotFSComp(module, params=module.params)
    changed, out, err = False, None, None
    if module.params["state"] == "present":
        changed, out, err = fscomp.create()
    else:
        changed, out, err = fscomp.destroy()
    module.exit_json(changed=changed, stdout=out, stderr=err)

if __name__ == "__main__":
    main()
