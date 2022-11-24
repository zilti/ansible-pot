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
    
    def create(self, tmp, task_vars):
        exists_path = self.pot_root(tmp, task_vars)+'/fscomp/'+self._task.args.get('name')
        cmd = ['$(which pot)', 'create-base']
        if self._task.args.get("name", None):
            cmd.append("-b")
            cmd.append('%s' % self._task.args.get("name", None))
        
        if self._task.args.get("release", None):
            cmd.append("-r")
            cmd.append('%s' % self._task.args.get("release", None))
        
        cmd = ' '.join(cmd)
        return self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True, creates=exists_path), task_vars=task_vars, tmp=tmp)
    
    def destroy(self, tmp, task_vars):
        exists_path = self.pot_root(tmp, task_vars)+'/fscomp/'+self._task.args.get('name')
        cmd = ['$(which pot)', 'destroy', '-br', self._task.args.get('name')]
        cmd = ' '.join(cmd)
        return self._execute_module(module_name='ansible.builtin.command', module_args=dict(_raw_params=cmd, _uses_shell=True, removes=exists_path), task_vars=task_vars, tmp=tmp)
    
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        state = self._task.args.get('state')
        if state == 'present':
            result.update(self.create(tmp, task_vars))
        if state == 'absent':
            result.update(self.destroy(tmp, task_vars))
        return result
