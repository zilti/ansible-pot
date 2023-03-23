# -*- Coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import os
import subprocess
from ansible.errors import AnsibleAction, AnsibleActionFail
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

display = Display()


class ActionModule(ActionBase):

    def pot_root(self, tmp, task_vars):
        display.vvv("Determining pot root...")
        result = self._execute_module(
            module_name='ansible.builtin.command',
            module_args=dict(_uses_shell=True,_raw_params='$(which pot) config -g fs_root'),
            task_vars=task_vars,
            tmp=tmp
        )
        display.vvv("Pot Root output: %s" % result['stdout'])
        return result['stdout'].split("=")[1].strip()
    
    def pot_zfs_root(self, tmp, task_vars):
        result = self._execute_module(
            module_name='ansible.builtin.command',
            module_args=dict(_uses_shell=True,_raw_params='$(which pot) config -g zfs_root'),
            task_vars=task_vars,
            tmp=tmp
        )
        return result['stdout'].split('=')[1].strip()
    
    def jail_exists(self, tmp, task_vars):
        cmd = ' '.join(['$(which pot)', 'ls'])
        display.vvv('Determining if jail exists')
        result = self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
        filtered = filter(lambda x: x.startswith("pot name"), result['stdout'].split("\n"))
        return self._task.args.get('name') in list(map(lambda x: x.split(":")[1].strip(), filtered))
    def get_info(self, tmp, task_vars, key):
        cmd = ' '.join(['$(which pot)', 'info', '-p', self._task.args.get('name')])
        result = self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
        splat = map(lambda x: x.strip(), result['stdout'].split("\n"))
        filtered = list(filter(lambda x: x.startswith(key), splat))
        return filtered[0].split(":")[1].strip()
    def has_mount(self, tmp, task_vars, mountpoint, mounttarget):
        jaildir = self.pot_root(tmp, task_vars)+'/jails/'+self._task.args.get('name')
        jailroot = jaildir+'/m'
        mountline = mounttarget+' '+jailroot+mountpoint
        cmd = ' '.join(['cat', jaildir+'/conf/fscomp.conf', '|', 'awk \'{ print $1 " " $2 }\''])
        result = self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
        res = list(filter(lambda x: x == mountline, result['stdout'].split("\n")))
        return len(res) > 0
    def create(self, result, tmp, task_vars):
        if self.jail_exists(tmp, task_vars):
            return result
        exists_path = self.pot_root(tmp, task_vars)+'/jails/'+self._task.args.get('name')
        cmd = ['$(which pot)', 'create']
        if self._task.args.get("name", None):
            cmd.append("-p")
            cmd.append('%s' % self._task.args.get("name", None))
        
        for elem in self._task.args.get("ip", []):
            cmd.append("-i")
            cmd.append('%s' % elem)
        
        if self._task.args.get("dns", None):
            cmd.append("-d")
            cmd.append('%s' % self._task.args.get("dns", None))
        
        if self._task.args.get("base", None):
            cmd.append("-b")
            cmd.append('%s' % self._task.args.get("base", None))
        
        if self._task.args.get("type", None):
            cmd.append("-t")
            cmd.append('%s' % self._task.args.get("type", None))
        
        for elem in self._task.args.get("flavour", ['ansible-managed']):
            cmd.append("-f")
            cmd.append('%s' % elem)
        
        if self._task.args.get("pot", None):
            cmd.append("-P")
            cmd.append('%s' % self._task.args.get("pot", None))
        
        if self._task.args.get("level", None):
            cmd.append("-l")
            cmd.append('%s' % self._task.args.get("level", None))
        
        if self._task.args.get("network_type", None):
            cmd.append("-N")
            cmd.append('%s' % self._task.args.get("network_type", None))
        
        if self._task.args.get("network_stack", None):
            cmd.append("-S")
            cmd.append('%s' % self._task.args.get("network_stack", None))
        
        if self._task.args.get("bridge_name", None):
            cmd.append("-B")
            cmd.append('%s' % self._task.args.get("bridge_name", None))
        
        display.vvv("Prepared jail creation command: %s" % cmd)
        cmd = ' '.join(cmd)
        self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True, creates=exists_path), task_vars=task_vars, tmp=tmp)
        result['changed'] = True
        return result
    def destroy(self, result, tmp, task_vars):
        if not self.jail_exists(tmp, task_vars):
            return result
        exists_path = self.pot_root(tmp, task_vars)+'/jails/'+self._task.args.get('name')
        cmd = ' '.join(['$(which pot)', 'destroy', '-rp', self._task.args.get('name')])
        self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True, removes=exists_path), task_vars=task_vars, tmp=tmp)
        result['changed'] = True
        return result
    def stop(self, result, tmp, task_vars):
        cmd = ' '.join(['$(which pot)', 'stop', self._task.args.get('name')])
        if self.get_info(tmp, task_vars, 'active') == 'true':
            self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
            result['changed'] = True
        return result
    def start(self, result, tmp, task_vars):
        cmd = ' '.join(['$(which pot)', 'start', self._task.args.get('name')])
        if self.get_info(tmp, task_vars, 'active') == 'false':
            self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
            result['changed'] = True
        return result
    def mounts(self, result, tmp, task_vars):
        mounts = self._task.args.get('mounts', None)
        if not mounts:
            return result
        for mount in mounts:
            mounttarget = ""
            if "dir" in mount:
                mounttarget = mount["dir"]
            elif "fscomp" in mount:
                mounttarget = self.pot_zfs_root(tmp, task_vars)+'/fscomp/'+mount["fscomp"]
            elif "dataset" in mount:
                mounttarget = mount["dataset"]
    
            if not self.has_mount(tmp, task_vars, mount["target"], mounttarget):
                cmd = ['$(which pot)', 'mount-in', '-p', self._task.args.get('name')]
                if "mode" in mount and mount["mode"] != "ro":
                    mount.pop("mode")
                if mount.get("target", None):
                    cmd.append("-m")
                    cmd.append('%s' % mount.get("target", None))
                
                if mount.get("dir", None):
                    cmd.append("-d")
                    cmd.append('%s' % mount.get("dir", None))
                
                if mount.get("fscomp", None):
                    cmd.append("-f")
                    cmd.append('%s' % mount.get("fscomp", None))
                
                if mount.get("dataset", None):
                    cmd.append("-z")
                    cmd.append('%s' % mount.get("dataset", None))
                
                if mount.get("direct", False):
                    cmd.append("-w")
                
                if mount.get("mode", False):
                    cmd.append("-r")
                
                cmd = ' '.join(cmd)
                result.update(self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp))
        return result
    def map_ports(self, result, tmp, task_vars):
        display.vvv('Mapping Jail Ports')
        ports = self._task.args.get('ports', None)
        if not ports:
            return result
        pmcmd = ['$(which pot)', 'export-ports', '-p', self._task.args.get('name')]
        portlist = []
        for port in ports:
            portstr = "{0}".format(port["port"])
            if "protocol" in port:
                portstr = "{0}:{1}".format(port["protocol"], portstr)
            if "pot_port" in port:
                portstr = "{0}:{1}".format(portstr, port["pot_port"])
            pmcmd.append('-e')
            pmcmd.append(portstr)
            portlist.append(portstr)
        cmd = ' '.join(['$(which pot)', 'info', '-vp', self._task.args.get('name')])
        out = self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
        out = list(filter(lambda x : 'exported ports' in x, out['stdout'].split('\n')))
        if len(out) > 0 and 'exported ports' in out[0]:
            out = out[0].split('exported ports:')[1].strip()
        else:
            out = ''
        display.vvv('Comparing %s with %s' % (out, ' '.join(portlist)))
        if out == ' '.join(portlist):
            return result
        cmd = ' '.join(pmcmd)
        self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
        result["changed"] = True
        return result
    def set_attributes(self, result, tmp, task_vars):
        display.vvv('Setting Jail Attributes')
        attrs = self._task.args.get('attributes', None)
        if not attrs:
            return result
        cmd = ' '.join(['$(which pot)', 'info', '-vp', self._task.args.get('name')])
        out = self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
        display.vvv('Splitting %s by "jail attributes:"' % out['stdout'])
        pot_attr_list = list(filter(lambda x: ':' in x, out['stdout'].split('jail attributes:')[1].split('\n')))
        pot_attrs = {}
        for pot_attr in pot_attr_list:
            display.vvv('Splitting %s' % pot_attr)
            pot_attr = pot_attr.split(':')
            pot_attr[0] = pot_attr[0].strip()
            pot_attr[1] = pot_attr[1].strip()
            if pot_attr[1] == 'YES':
                pot_attr[1] = True
            if pot_attr[1] == 'NO':
                pot_attr[1] = False
            pot_attrs[pot_attr[0]] = pot_attr[1]
        for attrk in attrs.keys():
            if attrs[attrk] in ['YES', 'Yes', 'yes', 'true', 'True', 'TRUE']:
                attrs[attrk] = True
            if attrs[attrk] in ['NO', 'No', 'no', 'false', 'False', 'FALSE']:
                attrs[attrk] = False
        for attrk in attrs.keys():
            if attrk in pot_attrs and pot_attrs[attrk] == attrs[attrk]:
                continue
            else:
                cmd = ' '.join(['$(which pot)', 'set-attribute', '-p', self._task.args.get('name'), '-A', attrk, '-V', '%s' % attrs[attrk]])
                newres = self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True), task_vars=task_vars, tmp=tmp)
                result['changed'] = result['changed'] or newres['changed']
        return result
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        state = self._task.args.get('state')
        if state in ['present', 'stopped', 'started', 'restarted']:
            result = self.create(result, tmp, task_vars)
        if state in ['stopped', 'restarted', 'absent']:
            result = self.stop(result, tmp, task_vars)
        if state in ['absent']:
            result = self.destroy(result, tmp, task_vars)
        if state != 'absent':
            result = self.mounts(result, tmp, task_vars)
            result = self.map_ports(result, tmp, task_vars)
            result = self.set_attributes(result, tmp, task_vars)
        if state in ['started', 'restarted']:
            result = self.start(result, tmp, task_vars)
        if state != 'absent':
            result['ip'] = self.get_info(tmp, task_vars, 'ip')
        return result
