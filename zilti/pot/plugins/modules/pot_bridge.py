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
module: pot_bridge
short_description: Pot bridge task.
version_added: 0.1.0
description:
  - Pot bridge task.
author: "Daniel Ziltener <dziltener@lyrion.ch>"
options:
  name:
      description:
        - The bridge name
      type: str
      required: True
      default: None
  size:
      description:
        - expected number of hosts
      type: int
      required: False
      default: None
  state:
      type: str
      required: False
      default: 'present'
      choices: [ 'present', 'absent' ]
  ignore:
      type: bool
      required: False
      default: False
  
requirements:
  - FreeBSD with Root-on-ZFS
"""

EXAMPLES = r"""
"""


class PotBridge(object):
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
    def bridge_exists(self):
        return exists(self.pot_root()+'/bridges/'+self.params["name"])
    def create(self):
        if self.params["state"] == "present" and not self.bridge_exists():
            cmd = [self.executable[0], "create-private-bridge"]
            if "name" in self.params and self.params["name"]:
                cmd.append("-B")
                cmd.append(self.params["name"])
            
            if "size" in self.params and self.params["size"]:
                cmd.append("-S")
                cmd.append(self.params["size"])
            
            rc, out, err = self._exec(cmd)
            return True, out, err
        else:
            return False, None, None
    def destroy(self):
        if self.params["state"] == "absent" and self.bridge_exists():
            cmd = [self.executable[0], "destroy", "-B", self.params["name"]]
            rc, out, err = self._exec(cmd)
            return True, out, err
        else:
            return False, None, None


def main():
    arg_spec = dict(
        name=dict(default=None, type=str),
        size=dict(default=None, type=int),
        state=dict(default='present', type=str, choices=['present', 'absent']),
        ignore=dict(default=False, type=bool))
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    bridge = PotBridge(module, params=module.params)
    changed, out, err = False, None, None
    if module.params["state"] == "present":
        changed, out, err = bridge.create()
    else:
        changed, out, err = bridge.destroy()
    module.exit_json(changed=changed, stdout=out, stderr=err)

if __name__ == "__main__":
    main()
