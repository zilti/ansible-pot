# -*- Coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
import pipes
from ansible.errors import AnsibleError
from ansible.plugins.connection.ssh import Connection as SSHConnection
from ansible.module_utils._text import to_text
from ansible.plugins.loader import get_shell_plugin
from ansible.utils.display import Display
from contextlib import contextmanager

display = Display()


__metaclass__ = type


DOCUMENTATION = r"""
---
author: Daniel Ziltener <dziltener@lyrion.ch>
name: pot
short_description: Run tasks in pots
description:
  - Run commands or put/fetch files from/to an existing pot
options:
  ansible_host:
      description:
        - Name of the jail
      type: str
      required: False
      default: inventory_hostname
  ansible_user:
      description:
        - User inside the jail to run as
      type: str
      required: False
  
"""

EXAMPLES = r"""
"""


class Connection(ConnectionBase):
    transport = 'zilti.pot.pot'
    has_pipelining = True
    has_tty = False

    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)
        self.executable = "/usr/local/bin/pot"
        self.jail = self._play_context.remote_host
    
        if os.geteuid() != 0:
            raise AnsibleError("jail connection requires running as root")
        if self.jail not in self.list_jails():
            raise AnsibleError("jail %s does not exist" % self.jail)
    def _exec(self, args, env={}):
        res = subprocess.run(
            args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode, res.stdout.decode('utf-8'), res.stderr.decode('utf-8')
    def list_jails(self):
        rc, out, err = self._exec([self.executable, 'ls'])
        filtered = filter(lambda x: x.startswith("pot name"), out.split("\n"))
        jailnames = map(lambda x: x.split(":")[1].strip(), filtered)
        return jailnames
    def exec_command(self, cmd, in_data=None, sudoable=False):
        super(Connection, self).exec_command(cmd, in_data, sudoable)
        display.vvv("In jail %s: exec %s" % (self.jail, cmd))
        rc, out, err = self._exec([self.executable, 'exec', '-p', self.jail, cmd])
        return rc, out, err
    def put_file(self, in_path, out_path):
        super(Connection, self).put_file(in_path, out_path)
        display.vvv("In jail %s: put %s to %s" % (self.jail, in_path, out_path))
        rc, out, err = self._exec([self.executable, 'copy-in', '-p', self.jail, '-s', in_path, '-d', out_path])
    def fetch_file(self, in_path, out_path):
        super(Connection, self).fetch_file(in_path, out_path)
        display.vvv("In jail %s: fetch %s to %s" % (self.jail, in_path, out_path))
        rc, out, err = self._exec([self.executable, 'copy-out', '-p', self.jail, '-s', in_path, '-d', out_path])
