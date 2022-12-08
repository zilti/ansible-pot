# -*- Coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
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
      description:
        - Defaults to auto
      type: list
      required: False
      default: []
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
      type: list
      required: False
      default: ['ansible-managed']
      elements: str
  mounts:
      description:
        - Things to mount
      type: list
      required: False
      default: []
      elements: dict
  ports:
      description:
        - Ports to map
      type: list
      required: False
      default: []
      elements: dict
  attributes:
      description:
        - Attributes
      type: dict
      required: False
      default: {}
  
requirements:
  - FreeBSD with Root-on-ZFS
"""

EXAMPLES = r"""
"""
