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
"""
