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
connection: sshjail
short_description: connect via ssh client binary to jail
description:
    - This connection plugin allows ansible to communicate to the target machines via normal ssh command line.
author: Austin Hyde (@austinhyde)
version_added: historical
options:
  host:
      description: Hostname/ip to connect to.
      default: ''
      vars:
           - name: inventory_hostname
           - name: ansible_host
           - name: ansible_ssh_host
           - name: delegated_vars['ansible_host']
           - name: delegated_vars['ansible_ssh_host']
  host_key_checking:
      description: Determines if ssh should check host keys
      type: boolean
      ini:
          - section: defaults
            key: 'host_key_checking'
          - section: ssh_connection
            key: 'host_key_checking'
            version_added: '2.5'
      env:
          - name: ANSIBLE_HOST_KEY_CHECKING
          - name: ANSIBLE_SSH_HOST_KEY_CHECKING
            version_added: '2.5'
      vars:
          - name: ansible_host_key_checking
            version_added: '2.5'
          - name: ansible_ssh_host_key_checking
            version_added: '2.5'
  password:
      description: Authentication password for the C(remote_user). Can be supplied as CLI option.
      vars:
          - name: ansible_password
          - name: ansible_ssh_pass
          - name: ansible_ssh_password
  sshpass_prompt:
      description: Password prompt that sshpass should search for. Supported by sshpass 1.06 and up
      default: ''
      ini:
          - section: 'ssh_connection'
            key: 'sshpass_prompt'
      env:
          - name: ANSIBLE_SSHPASS_PROMPT
      vars:
          - name: ansible_sshpass_prompt
      version_added: '2.10'
  ssh_args:
      description: Arguments to pass to all ssh cli tools
      default: '-C -o ControlMaster=auto -o ControlPersist=60s'
      ini:
          - section: 'ssh_connection'
            key: 'ssh_args'
      env:
          - name: ANSIBLE_SSH_ARGS
      vars:
          - name: ansible_ssh_args
            version_added: '2.7'
  ssh_common_args:
      description: Common extra args for all ssh CLI tools
      ini:
          - section: 'ssh_connection'
            key: 'ssh_common_args'
            version_added: '2.7'
      env:
          - name: ANSIBLE_SSH_COMMON_ARGS
            version_added: '2.7'
      vars:
          - name: ansible_ssh_common_args
      cli:
          - name: ssh_common_args
  ssh_executable:
      default: ssh
      description:
        - This defines the location of the ssh binary. It defaults to ``ssh`` which will use the first ssh binary available in $PATH.
        - This option is usually not required, it might be useful when access to system ssh is restricted,
          or when using ssh wrappers to connect to remote hosts.
      env: [{name: ANSIBLE_SSH_EXECUTABLE}]
      ini:
      - {key: ssh_executable, section: ssh_connection}
      #const: ANSIBLE_SSH_EXECUTABLE
      version_added: "2.2"
      vars:
          - name: ansible_ssh_executable
            version_added: '2.7'
  sftp_executable:
      default: sftp
      description:
        - This defines the location of the sftp binary. It defaults to ``sftp`` which will use the first binary available in $PATH.
      env: [{name: ANSIBLE_SFTP_EXECUTABLE}]
      ini:
      - {key: sftp_executable, section: ssh_connection}
      version_added: "2.6"
      vars:
          - name: ansible_sftp_executable
            version_added: '2.7'
  scp_executable:
      default: scp
      description:
        - This defines the location of the scp binary. It defaults to `scp` which will use the first binary available in $PATH.
      env: [{name: ANSIBLE_SCP_EXECUTABLE}]
      ini:
      - {key: scp_executable, section: ssh_connection}
      version_added: "2.6"
      vars:
          - name: ansible_scp_executable
            version_added: '2.7'
  scp_extra_args:
      description: Extra exclusive to the ``scp`` CLI
      vars:
          - name: ansible_scp_extra_args
      env:
        - name: ANSIBLE_SCP_EXTRA_ARGS
          version_added: '2.7'
      ini:
        - key: scp_extra_args
          section: ssh_connection
          version_added: '2.7'
      cli:
        - name: scp_extra_args
      default: ''
  sftp_extra_args:
      description: Extra exclusive to the ``sftp`` CLI
      vars:
          - name: ansible_sftp_extra_args
      env:
        - name: ANSIBLE_SFTP_EXTRA_ARGS
          version_added: '2.7'
      ini:
        - key: sftp_extra_args
          section: ssh_connection
          version_added: '2.7'
      cli:
        - name: sftp_extra_args
      default: ''
  ssh_extra_args:
      description: Extra exclusive to the 'ssh' CLI
      vars:
          - name: ansible_ssh_extra_args
      env:
        - name: ANSIBLE_SSH_EXTRA_ARGS
          version_added: '2.7'
      ini:
        - key: ssh_extra_args
          section: ssh_connection
          version_added: '2.7'
      cli:
        - name: ssh_extra_args
      default: ''
  reconnection_retries:
      description: Number of attempts to connect.
      default: 0
      type: integer
      env:
        - name: ANSIBLE_SSH_RETRIES
      ini:
        - section: connection
          key: retries
        - section: ssh_connection
          key: retries
      vars:
        - name: ansible_ssh_retries
          version_added: '2.7'
  port:
      description: Remote port to connect to.
      type: int
      ini:
        - section: defaults
          key: remote_port
      env:
        - name: ANSIBLE_REMOTE_PORT
      vars:
        - name: ansible_port
        - name: ansible_ssh_port
      keyword:
        - name: port
  remote_user:
      description:
          - User name with which to login to the remote server, normally set by the remote_user keyword.
          - If no user is supplied, Ansible will let the ssh client binary choose the user as it normally
      ini:
        - section: defaults
          key: remote_user
      env:
        - name: ANSIBLE_REMOTE_USER
      vars:
        - name: ansible_user
        - name: ansible_ssh_user
      cli:
        - name: user
      keyword:
        - name: remote_user
  pipelining:
      default: ANSIBLE_PIPELINING
      description:
        - Pipelining reduces the number of SSH operations required to execute a module on the remote server,
          by executing many Ansible modules without actual file transfer.
        - This can result in a very significant performance improvement when enabled.
        - However this conflicts with privilege escalation (become).
          For example, when using sudo operations you must first disable 'requiretty' in the sudoers file for the target hosts,
          which is why this feature is disabled by default.
      env:
        - name: ANSIBLE_PIPELINING
        - name: ANSIBLE_SSH_PIPELINING
      ini:
        - section: defaults
          key: pipelining
        - section: ssh_connection
          key: pipelining
      type: boolean
      vars:
        - name: ansible_pipelining
        - name: ansible_ssh_pipelining
  private_key_file:
      description:
          - Path to private key file to use for authentication
      ini:
        - section: defaults
          key: private_key_file
      env:
        - name: ANSIBLE_PRIVATE_KEY_FILE
      vars:
        - name: ansible_private_key_file
        - name: ansible_ssh_private_key_file
      cli:
        - name: private_key_file
          option: '--private-key'
  control_path:
    description:
      - This is the location to save ssh's ControlPath sockets, it uses ssh's variable substitution.
      - Since 2.3, if null, ansible will generate a unique hash. Use `%(directory)s` to indicate where to use the control dir path setting.
    env:
      - name: ANSIBLE_SSH_CONTROL_PATH
    ini:
      - key: control_path
        section: ssh_connection
    vars:
      - name: ansible_control_path
        version_added: '2.7'
  control_path_dir:
    default: ~/.ansible/cp
    description:
      - This sets the directory to use for ssh control path if the control path setting is null.
      - Also, provides the `%(directory)s` variable for the control path setting.
    env:
      - name: ANSIBLE_SSH_CONTROL_PATH_DIR
    ini:
      - section: ssh_connection
        key: control_path_dir
    vars:
      - name: ansible_control_path_dir
        version_added: '2.7'
  sftp_batch_mode:
    default: 'yes'
    description: 'TODO: write it'
    env: [{name: ANSIBLE_SFTP_BATCH_MODE}]
    ini:
    - {key: sftp_batch_mode, section: ssh_connection}
    type: bool
    vars:
      - name: ansible_sftp_batch_mode
        version_added: '2.7'
  ssh_transfer_method:
    default: smart
    description:
        - "Preferred method to use when transferring files over ssh"
        - Setting to 'smart' (default) will try them in order, until one succeeds or they all fail
        - Using 'piped' creates an ssh pipe with ``dd`` on either side to copy the data
    choices: ['sftp', 'scp', 'piped', 'smart']
    env: [{name: ANSIBLE_SSH_TRANSFER_METHOD}]
    ini:
        - {key: transfer_method, section: ssh_connection}
    vars:
        - name: ansible_ssh_transfer_method
          version_added: '2.12'
  scp_if_ssh:
    default: smart
    description:
      - "Prefered method to use when transfering files over ssh"
      - When set to smart, Ansible will try them until one succeeds or they all fail
      - If set to True, it will force 'scp', if False it will use 'sftp'
    env: [{name: ANSIBLE_SCP_IF_SSH}]
    ini:
    - {key: scp_if_ssh, section: ssh_connection}
    vars:
      - name: ansible_scp_if_ssh
        version_added: '2.7'
  use_tty:
    version_added: '2.5'
    default: 'yes'
    description: add -tt to ssh commands to force tty allocation
    env: [{name: ANSIBLE_SSH_USETTY}]
    ini:
    - {key: usetty, section: ssh_connection}
    type: bool
    vars:
      - name: ansible_ssh_use_tty
        version_added: '2.7'
  pkcs11_provider:
    version_added: '2.12'
    default: ''
    description:
      - PKCS11 SmartCard provider such as opensc, example: /usr/local/lib/opensc-pkcs11.so
      - Requires sshpass version 1.06+, sshpass must support the -P option.
    env: [{name: ANSIBLE_PKCS11_PROVIDER}]
    ini:
      - {key: pkcs11_provider, section: ssh_connection}
    vars:
      - name: ansible_ssh_pkcs11_provider
  timeout:
    default: 10
    description:
        - This is the default ammount of time we will wait while establishing an ssh connection
        - It also controls how long we can wait to access reading the connection once established (select on the socket)
    env:
        - name: ANSIBLE_TIMEOUT
        - name: ANSIBLE_SSH_TIMEOUT
          version_added: '2.11'
    ini:
        - key: timeout
          section: defaults
        - key: timeout
          section: ssh_connection
          version_added: '2.11'
    vars:
        - name: ansible_ssh_timeout
          version_added: '2.11'
    cli:
        - name: timeout
    type: integer
"""

EXAMPLES = r"""
"""


class ConnectionBase(SSHConnection):
    pass

class Connection(ConnectionBase):
    transport = 'zilti.pot.pot_remote'

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args,**kwargs)
        # self.host == jailname@jailhost
        self.inventory_hostname = self.host
        self.jailspec, self.host = self.host.split('@', 1)
        # self.jailspec == jailname
        # self.host == jailhost
        # this way SSHConnection parent class uses the jailhost as the SSH remote host

        self.executable = "/usr/local/bin/pot"
        if self.jailspec not in self.list_jails():
            raise AnsibleError("jail %s does not exist in %s on host %s" % (self.jailspec, self.list_jails(), self.host))

    def list_jails(self):
        rc, out, err = self._jailhost_command(" ".join([self.executable, 'ls']))
        out = out.decode('utf-8')
        filtered = filter(lambda x: x.startswith("pot name"), out.split("\n"))
        jailnames = list(map(lambda x: x.split(":")[1].strip(), filtered))
        return jailnames

    def pot_root(self):
        rc, out, err = self._jailhost_command(" ".join([self.executable, 'config', '-g', 'fs_root']))
        return out.decode('utf-8').split("=")[1].strip()

    def jail_prefix(self):
        rc, out, err = self._jailhost_command(' '.join([self.executable, 'config', '-g', 'pot_prefix']))
        return out.decode('utf-8').split("=")[1].strip()

    def _strip_sleep(self, cmd):
        # Get the command without sleep
        cmd = cmd.split(' && sleep 0', 1)[0]
        # Add back trailing quote
        cmd = '%s%s' % (cmd, "'")
        return cmd

    def _jailhost_command(self, cmd):
        return super(Connection, self).exec_command(cmd, in_data=None, sudoable=True)

    def exec_command(self, cmd, in_data=None, executable='/bin/sh', sudoable=True):
        slpcmd = False

        if '&& sleep 0' in cmd:
            slpcmd = True
            cmd = self._strip_sleep(cmd)

        cmd = ' '.join([executable, '-c', pipes.quote(cmd)])
        display.vvv("NEW COMMAND: {0}".format(cmd))
        if slpcmd:
            cmd = " ".join([self.executable, 'exec', '-p', self.jailspec, cmd, '&& sleep 0'])
        else:
            cmd = " ".join([self.executable, 'exec', '-p', self.jailspec, cmd])

        plugin = self.become
        shell = get_shell_plugin(executable=executable)
        cmd = plugin.build_become_command(cmd, shell)

        display.vvv(u"EXEC {0}".format(cmd))
        rc, out, err = super(Connection, self).exec_command(cmd, in_data, True)
        display.vvv(u"RESULT {0} ERR {1}".format(out, err))
        return rc, out, err

    @contextmanager
    def tempfile(self):
        code, stdout, stderr = self._jailhost_command('mktemp')
        if code != 0:
            raise AnsibleError("failed to make temp file:\n%s\n%s" % (stdout, stderr))
        tmp = to_text(stdout.strip().split(b'\n')[-1])

        code, stdout, stderr = self._jailhost_command(' '.join(['chmod 0644', tmp]))
        if code != 0:
            raise AnsibleError("failed to make temp file %s world readable:\n%s\n%s" % (tmp, stdout, stderr))

        yield tmp

        code, stdout, stderr = self._jailhost_command(' '.join(['rm', tmp]))
        if code != 0:
            raise AnsibleError("failed to remove temp file %s:\n%s\n%s" % (tmp, stdout, stderr))

    def _normalize_path(self, path, prefix='/'):
        if path.startswith("~"):
            path = "/root/{0}".format(path)
        if not path.startswith(os.path.sep):
            path = os.path.join(os.path.sep, path)
        normpath = os.path.normpath(path)
        return os.path.join(prefix, normpath[1:])

    def _copy_file(self, direction, from_file, to_file, executable='/bin/sh'):
        copycmd= ' '.join([self.executable, 'copy-'+direction, '-F', '-p', self.jailspec, '-s', from_file, '-d', to_file])
#        if self._play_context.become:
        plugin = self.become
        shell = get_shell_plugin(executable=executable)
        copycmd = plugin.build_become_command(copycmd, shell)

        display.vvv(u"REMOTE COPY {0} TO {1}".format(from_file, to_file), host=self.inventory_hostname)
        code, stdout, stderr = self._jailhost_command(copycmd)
        if code != 0:
            raise AnsibleError("failed to copy file from %s to %s:\n%s\n%s" % (from_file, to_file, stdout, stderr))

    def put_file(self, in_path, out_path):
        ''' transfer a file from local to remote jail '''
        out_path = self._normalize_path(out_path)#, "%s/jails/%s/m" % (self.pot_root(), self.jailspec))

        with self.tempfile() as tmp:
            super(Connection, self).put_file(in_path, tmp)
            display.vvv("Jail %s: putting %s to %s" % (self.jailspec, tmp, out_path))
            self._copy_file('in', tmp, out_path)

    def fetch_file(self, in_path, out_path):
        ''' fetch a file from remote to local '''
        in_path = self._normalize_path(in_path)#, "%s/jails/%s/m" % (self.pot_root(), self.jailspec))

        with self.tempfile() as tmp:
            display.vvv("Jail %s: fetching %s to %s" % (self.jailspec, in_path, tmp))
            self._copy_file('out', in_path, tmp)
            super(Connection, self).fetch_file(tmp, out_path)
