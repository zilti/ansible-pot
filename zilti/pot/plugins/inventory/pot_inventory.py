# -*- Coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import os
import re
import subprocess

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.utils.display import Display

display = Display()


class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'zilti.pot.pot'

    def _populate(self):


    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path=path)
