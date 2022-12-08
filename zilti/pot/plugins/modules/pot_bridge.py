# -*- Coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
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
- name: Create private bridge
  pot_bridge:
    name: mybridge
    size: 5
- name: Check if creation was successful
  shell:
    cmd: if [ -f /opt/pot/bridges/mybridge ]; then exit 0; else exit 1; fi
  register: bridgetest
- name: Assert test result
  assert:
    that:
      - bridgetest.rc == 0
"""
