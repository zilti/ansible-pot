# -*- Coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import re
import subprocess
from os.path import exists
from ansible.module_utils.basic import AnsibleModule
from ansible.errors import AnsibleError


__metaclass__ = type


DOCUMENTATION = r"""
---
module: pot_jail
short_description: Pot jail task.
version_added: 0.1.0
description:
  - Pot jail task.
author: "Daniel Ziltener <dziltener@lyrion.ch>"
options:
  name:
      description:
        - The jail name
      type: str
      required: True
      default: None
  state:
      type: str
      required: False
      default: 'present'
      choices: [ 'present', 'absent', 'started', 'stopped', 'restarted' ]
  ignore:
      description:
        - Ignore this task?
      type: bool
      required: False
      default: False
  ip:
      type: list
      required: False
      default: None
      elements: str
  network_stack:
      type: str
      required: False
      default: 'dual'
      choices: [ 'ipv4', 'ipv6', 'dual' ]
  network_type:
      type: str
      required: False
      default: 'inherit'
      choices: [ 'inherit', 'alias', 'public-bridge', 'private-bridge' ]
  bridge_name:
      type: str
      required: False
      default: None
  base:
      type: str
      required: True
      default: None
  pot:
      type: str
      required: False
      default: None
  type:
      type: str
      required: False
      default: 'multi'
      choices: [ 'single', 'multi' ]
  level:
      type: int
      required: False
      default: None
  flavour:
      type: str
      required: False
      default: None
  mounts:
      description:
        - Things to mount
      type: list
      required: False
      default: []
      elements: dict
  
requirements:
  - FreeBSD with Root-on-ZFS
"""

EXAMPLES = r"""
"""


class PotJail(object):
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
    def jail_exists(self):
        cmd = [self.executable[0], "ls"]
        rc, out, err = self._exec(cmd)
        filtered = filter(lambda x: x.startswith("pot name"), out.split("\n"))
        return self.params["name"] in map(lambda x: x.split(":")[1].strip(), filtered)
    def has_mount(self, mountpoint, mounttarget):
        jaildir = self.pot_root()+'/jails/'+self.params["name"]
        jailroot = jaildir+'/m'
        mountline = mounttarget+' '+jailroot+mountpoint
        rc, out, err = self._exec(['cat', jaildir+'/conf/fscomp.conf'])
        res = list(filter(lambda x: x == mountline, out.split("\n")))
        return len(res) > 0
    def create(self):
        if self.params["state"] in ['present', 'started', 'stopped', 'restarted'] and not self.jail_exists():
            cmd = [self.executable[0], "create"]
            if "name" in self.params and self.params["name"]:
                cmd.append("-p")
                cmd.append(self.params["name"])
            
            for elem in self.params["ip"]:
                cmd.append("-i")
                cmd.append(elem)
            
            if "dns" in self.params and self.params["dns"]:
                cmd.append("-d")
                cmd.append(self.params["dns"])
            
            if "base" in self.params and self.params["base"]:
                cmd.append("-b")
                cmd.append(self.params["base"])
            
            if "type" in self.params and self.params["type"]:
                cmd.append("-t")
                cmd.append(self.params["type"])
            
            if "flavour" in self.params and self.params["flavour"]:
                cmd.append("-f")
                cmd.append(self.params["flavour"])
            
            if "pot" in self.params and self.params["pot"]:
                cmd.append("-P")
                cmd.append(self.params["pot"])
            
            if "level" in self.params and self.params["level"]:
                cmd.append("-l")
                cmd.append(self.params["level"])
            
            if "network_type" in self.params and self.params["network_type"]:
                cmd.append("-N")
                cmd.append(self.params["network_type"])
            
            if "network_stack" in self.params and self.params["network_stack"]:
                cmd.append("-S")
                cmd.append(self.params["network_stack"])
            
            if "bridge_name" in self.params and self.params["bridge_name"]:
                cmd.append("-B")
                cmd.append(self.params["bridge_name"])
            
            rc, out, err = self._exec(cmd)
            return True, out, err
        else:
            return False, None, None
    def destroy(self):
        if self.params["state"] == 'absent' and self.jail_exists():
            cmd = [self.executable[0], "stop", self.params["name"]]
            self._exec(cmd)
            rc, out, err = self._exec([self.executable[0], "destroy", "-rp", self.params["name"]])
            return True, out, err
        else:
            return False, None, None
    def stop(self):
        if self.params["state"] in ['present', 'stopped', 'restarted'] and self.get_info('active') == 'true':
            cmd = [self.executable[0], "stop", self.params["name"]]
            rc, out, err = self._exec(cmd)
            return True, out, err
        else:
            return False, None, None
    def start(self):
        if self.params["state"] in ['started', 'restarted'] and self.get_info('active') == 'false':
            cmd = [self.executable[0], "start", self.params["name"]]
            rc, out, err = self._exec(cmd)
            return True, out, err
        else:
            return False, None, None
    def mounts(self):
        changed = False
        rc = 0
        out = None
        err = None
        if not "mounts" in self.params:
            return False, None, None
        for mount in self.params["mounts"]:
            mounttarget = ""
            if "dir" in mount:
                mounttarget = mount["dir"]
            elif "fscomp" in mount:
                mounttarget = self.pot_zfs_root()+'/fscomp/'+mount["fscomp"]
            elif "dataset" in mount:
                mounttarget = mount["dataset"]
    
            if not self.has_mount(mount["target"], mounttarget):
                cmd = [self.executable[0], 'mount-in', '-p', self.params["name"]]
                if "mode" in mount and mount["mode"] != "ro":
                    self.params.pop("mode")
                if "target" in mount and mount["target"]:
                    cmd.append("-m")
                    cmd.append(mount["target"])
                
                if "dir" in mount and mount["dir"]:
                    cmd.append("-d")
                    cmd.append(mount["dir"])
                
                if "fscomp" in mount and mount["fscomp"]:
                    cmd.append("-f")
                    cmd.append(mount["fscomp"])
                
                if "dataset" in mount and mount["dataset"]:
                    cmd.append("-z")
                    cmd.append(mount["dataset"])
                
                if "direct" in mount and mount["direct"]:
                    cmd.append("-w")
                
                if "mode" in mount and mount["mode"]:
                    cmd.append("-r")
                
                rc1, out1, err1 = self._exec(cmd)
                rc = rc + rc1
                out = (out and out+"\n"+out1) or out1
                err = (err and err+"\n"+err1) or err1
                changed = changed or True
            else:
                changed = changed or False
        return changed, out, err


def main():
    arg_spec = dict(
        name=dict(default=None, type="str"),
        state=dict(default='present', type="str", choices=['present', 'absent', 'started', 'stopped', 'restarted']),
        ignore=dict(default=False, type="bool"),
        ip=dict(default=None, type="list", elements="str"),
        network_stack=dict(default='dual', type="str", choices=['ipv4', 'ipv6', 'dual']),
        network_type=dict(default='inherit', type="str", choices=['inherit', 'alias', 'public-bridge', 'private-bridge']),
        bridge_name=dict(default=None, type="str"),
        base=dict(default=None, type="str"),
        pot=dict(default=None, type="str"),
        type=dict(default='multi', type="str", choices=['single', 'multi']),
        level=dict(default=None, type="int"),
        flavour=dict(default=None, type="str"),
        mounts=dict(default=[], type="list", elements="dict"))
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    jail = PotJail(module, params=module.params)
    changed, out, err = False, None, None
    if module.params["state"] == "present":
        changed, out, err = jail.create()
    elif module.params["state"] == "absent":
        changed, out, err = jail.destroy()
    elif module.params["state"] == "started":
        c1, o1, e1 = jail.create()
        c2, o2, e2 = jail.start()
        changed = c1 or c2
        out = "%s\n%s" % o1, o2
        err = "%s\n%s" % e1, e2
    elif module.params["state"] == "stopped":
        c1, o1, e1 = jail.create()
        c2, o2, e2 = jail.stop()
        changed = c1 or c2
        out = "%s\n%s" % o1, o2
        err = "%s\n%s" % e1, e2
    elif module.params["state"] == "restarted":
        c1, o1, e1 = jail.create()
        c2, o2, e2 = jail.stop()
        c3, o3, e3 = jail.start()
        changed = c1 or c2 or c3
        out = "%s\n%s\n%s" % o1, o2, o3
        err = "%s\n%s\n%s" % e1, e2, e3
    if module.params["state"] != "absent":
        c1, o1, e1 = jail.mounts()
        changed = changed or c1
        out = (out and out+"\n"+o1) or o1
        err = (err and err+"\n"+e1) or e1
    module.exit_json(changed=changed, stdout=out, stderr=err)


if __name__ == "__main__":
    main()
