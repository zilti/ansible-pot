
# Table of Contents

1.  [Requirements](#orga2a93a0)
2.  [Role Variables](#org50b6af0)
    1.  [Pot Server](#org10c0afd)
    2.  [Collected Variables](#org466f02a)
    3.  [Pot Configuration Template](#org9b8251c)
3.  [Plugins](#orgcda5a94)
    1.  [Bridges Module](#orga73a0b9)
    2.  [FS Components Module](#org692d971)
    3.  [Bases Module](#orgd78002c)
    4.  [Jails Module](#org6a51e8d)
    5.  [Inventory](#org0ecc845)
    6.  [Pot Connection](#org071f6b5)
    7.  [Lookup Plugin](#org2b02075)
4.  [Dependencies](#orgd149cdf)
5.  [Example Playbook](#org93776f5)
6.  [License](#org28db34f)
7.  [Author Information](#org6d6357e)
8.  [Ansible Galaxy Metadata](#orgd45118d)

I am a role to manage your Pot jails on FreeBSD. My source is located in the [pot.org](https://github.com/zilti/ansible-pot/blob/master/pot.org) file.


<a id="orga2a93a0"></a>

# Requirements

None.


<a id="org50b6af0"></a>

# Role Variables


<a id="org10c0afd"></a>

## Pot Server

<table id="org72feb7e" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">enabled</td>
<td class="org-left">bool</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">False</td>
<td class="org-left">Triggers <code>pot init</code></td>
</tr>


<tr>
<td class="org-left">vnet<sub>enabled</sub></td>
<td class="org-left">bool</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">False</td>
<td class="org-left">Triggers <code>pot vnet-start</code></td>
</tr>


<tr>
<td class="org-left">zfs<sub>root</sub></td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'tank/pot'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">fs<sub>root</sub></td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'/opt/pot'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">cache</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'/var/cache/pot'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">tmp</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'/tmp'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">mktemp<sub>suffix</sub></td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'.XXXXXXXX'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">hostname<sub>max</sub><sub>length</sub></td>
<td class="org-left">int</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">64</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">network</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'10.192.0.0/10'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">netmask</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'255.192.0.0'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">gateway</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'10.192.0.1'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>


<tr>
<td class="org-left">extif</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">'em0'</td>
<td class="org-left">Is written to <code>pot.conf</code></td>
</tr>
</tbody>
</table>

    ---
    pot:
      enabled: False
      vnet_enabled: False
      zfs_root: 'tank/pot'
      fs_root: '/opt/pot'
      cache: '/var/cache/pot'
      tmp: '/tmp'
      mktemp_suffix: '.XXXXXXXX'
      hostname_max_length: 64
      network: '10.192.0.0/10'
      netmask: '255.192.0.0'
      gateway: '10.192.0.1'
      extif: 'em0'


<a id="org466f02a"></a>

## Collected Variables

<table id="org85e7256" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">initialized</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">If <code>pot init</code> has been run already.</td>
</tr>


<tr>
<td class="org-left">vnet<sub>initialized</sub></td>
<td class="org-left">&#xa0;</td>
<td class="org-left">If <code>pot vnet-start</code> has been run already.</td>
</tr>


<tr>
<td class="org-left">version</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">The pot version.</td>
</tr>


<tr>
<td class="org-left">fscomps</td>
<td class="org-left">[]</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">bridges</td>
<td class="org-left">[]</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">bases</td>
<td class="org-left">[]</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">jails</td>
<td class="org-left">{}</td>
<td class="org-left">A JSON list of the data returned by <code>pot info -p</code>; keys are the jail names.</td>
</tr>
</tbody>
</table>

    ---
    potintel:
      initialized: '{{ ansible_local.pot.initialized|default("") }}'
      vnet_initialized: '{{ ansible_local.pot.vnet_initialized|default("") }}'
      version: '{{ ansible_local.pot.version|default("") }}'
      fscomps: '{{ ansible_local.pot.fscomps|default("[]") }}'
      bridges: '{{ ansible_local.pot.bridges|default("[]") }}'
      bases: '{{ ansible_local.pot.bases|default("[]") }}'
      jails: '{{ ansible_local.pot.jails|default("{}") }}'


<a id="org9b8251c"></a>

## Pot Configuration Template

    # {{ ansible_managed }}
    # pot configuration file
    
    # All datasets related to pot use the some zfs dataset as parent
    # With this variable, you can choose which dataset has to be used
    POT_ZFS_ROOT={{ pot.zfs_root|default("zroot/pot") }}
    
    # It is also important to know where the root dataset is mounted
    POT_FS_ROOT={{ pot.fs_root|default("/opt/pot") }}
    
    # This is the cache used to import/export pots
    POT_CACHE={{ pot.cache|default("/var/cache/pot") }}
    
    # This is where pot is going to store temporary files
    POT_TMP={{ pot.tmp|default("/tmp") }}
    
    # This is the suffix added to temporary files created using mktemp,
    # X is a placeholder for a random character, see mktemp(1)
    POT_MKTEMP_SUFFIX={{ pot.mktemp_suffix|default(".XXXXXXXX") }}
    
    # Define the max length of the hostname inside the pot
    POT_HOSTNAME_MAX_LENGTH={{ pot.hostname_max_length|default(64) }}
    
    # Internal Virtual Network configuration
    
    # IPv4 Internal Virtual network
    POT_NETWORK={{ pot.network|default("10.192.0.0/10") }}
    
    # Internal Virtual Network netmask
    POT_NETMASK={{ pot.netmask|default("255.192.0.0") }}
    
    # The default gateway of the Internal Virtual Network
    POT_GATEWAY={{ pot.gateway|default("10.192.0.1") }}
    
    # The name of the network physical interface, to be used as default gateway
    POT_EXTIF={{ pot.extif|default("em0") }}
    
    {% if "extra_extif" in pot %}
    # The list of extra network interface, to make other network segments accessible
    POT_EXTRA_EXTIF={%- for item in pot.extra_extif %}{{ item.name }} {%- endfor %}
    # for each extra interface, a variable is used to sepcify its network segment
    {% for item in pot.extra_extif %}
    POT_NETWORK_{{ item.name }}={{ item.netmask }}
    {% endfor %}
    {% else %}
    # POT_EXTRA_EXTIF=expl0
    # POT_NETWORK_expl0=
    {% endif %}
    
    # DNS on the Internal Virtual Network
    
    # name of the pot running the DNS
    POT_DNS_NAME={{ pot.dns_name|default() }}
    
    # IP of the DNS
    POT_DNS_IP={{ pot.dns_ip|default() }}
    
    # VPN support
    
    # name of the tunnel network interface
    POT_VPN_EXTIF={{ pot.vpn_extif|default() }}
    
    {% if "vpn_networks" in pot %}
    POT_VPN_NETWORKS={%- for item in pot.vpn_networks %}{{ item }} {%- endfor %}
    {% else %}
    # POT_VPN_NETWORKS=
    {% endif %}
    
    # EOF


<a id="orgcda5a94"></a>

# Plugins


<a id="orga73a0b9"></a>

## Bridges Module

Pot bridges created with `pot create-private-bridge`.

<table id="orgba99ad8" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">name</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">The bridge name</td>
</tr>


<tr>
<td class="org-left">size</td>
<td class="org-left">int</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">expected number of hosts</td>
</tr>


<tr>
<td class="org-left">state</td>
<td class="org-left">str</td>
<td class="org-left">'present', 'absent'</td>
<td class="org-left">#f</td>
<td class="org-left">'present'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">ignore</td>
<td class="org-left">bool</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">False</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>


### Examples

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


<a id="org692d971"></a>

## FS Components Module

The ones created with `pot create-fscomp`.

<table id="orgd85bd8b" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">name</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">The fscomp name</td>
</tr>


<tr>
<td class="org-left">state</td>
<td class="org-left">str</td>
<td class="org-left">'present', 'absent'</td>
<td class="org-left">#f</td>
<td class="org-left">'present'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">ignore</td>
<td class="org-left">bool</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">False</td>
<td class="org-left">Ignore this task?</td>
</tr>
</tbody>
</table>


### Examples


<a id="orgd78002c"></a>

## Bases Module

The ones created with `pot create-base`.

<table id="orgb904244" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">name</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">The base name</td>
</tr>


<tr>
<td class="org-left">release</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">The FreeBSD release to use</td>
</tr>


<tr>
<td class="org-left">state</td>
<td class="org-left">str</td>
<td class="org-left">'present', 'absent'</td>
<td class="org-left">#f</td>
<td class="org-left">'present'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">ignore</td>
<td class="org-left">bool</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">False</td>
<td class="org-left">Ignore this task?</td>
</tr>
</tbody>
</table>


### Examples


<a id="org6a51e8d"></a>

## Jails Module

For each jail, you can supply a number of arguments.

<table id="org1611286" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">name</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">The jail name</td>
</tr>


<tr>
<td class="org-left">state</td>
<td class="org-left">str</td>
<td class="org-left">'present', 'absent', 'started', 'stopped', 'restarted'</td>
<td class="org-left">#f</td>
<td class="org-left">'present'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">ignore</td>
<td class="org-left">bool</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">False</td>
<td class="org-left">Ignore this task?</td>
</tr>


<tr>
<td class="org-left">ip</td>
<td class="org-left">list</td>
<td class="org-left">str</td>
<td class="org-left">#f</td>
<td class="org-left">[]</td>
<td class="org-left">Defaults to auto</td>
</tr>


<tr>
<td class="org-left">network<sub>stack</sub></td>
<td class="org-left">str</td>
<td class="org-left">'ipv4', 'ipv6', 'dual'</td>
<td class="org-left">#f</td>
<td class="org-left">'dual'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">network<sub>type</sub></td>
<td class="org-left">str</td>
<td class="org-left">'inherit', 'alias', 'public-bridge', 'private-bridge'</td>
<td class="org-left">#f</td>
<td class="org-left">'inherit'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">bridge<sub>name</sub></td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">base</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">pot</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">type</td>
<td class="org-left">str</td>
<td class="org-left">'single', 'multi'</td>
<td class="org-left">#f</td>
<td class="org-left">'multi'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">level</td>
<td class="org-left">int</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">flavour</td>
<td class="org-left">list</td>
<td class="org-left">str</td>
<td class="org-left">#f</td>
<td class="org-left">['ansible-managed']</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">mounts</td>
<td class="org-left">list</td>
<td class="org-left">dict</td>
<td class="org-left">#f</td>
<td class="org-left">[]</td>
<td class="org-left">Things to mount</td>
</tr>


<tr>
<td class="org-left">ports</td>
<td class="org-left">list</td>
<td class="org-left">dict</td>
<td class="org-left">#f</td>
<td class="org-left">[]</td>
<td class="org-left">Ports to map</td>
</tr>


<tr>
<td class="org-left">attributes</td>
<td class="org-left">dict</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">{}</td>
<td class="org-left">Attributes</td>
</tr>
</tbody>
</table>

**Options for mounts:**

<table id="org67abd92" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">target</td>
<td class="org-left">path</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">Mount point</td>
</tr>


<tr>
<td class="org-left">dir</td>
<td class="org-left">path</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">Directory on the host to mount</td>
</tr>


<tr>
<td class="org-left">fscomp</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">fscomp to mount</td>
</tr>


<tr>
<td class="org-left">dataset</td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">ZFS dataset to mount</td>
</tr>


<tr>
<td class="org-left">direct</td>
<td class="org-left">bool</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">False</td>
<td class="org-left">change the ZFS mount point instead of using nullfs</td>
</tr>


<tr>
<td class="org-left">mode</td>
<td class="org-left">str</td>
<td class="org-left">'ro', 'rw'</td>
<td class="org-left">#f</td>
<td class="org-left">'rw'</td>
<td class="org-left">Mount as read-only or read-write?</td>
</tr>
</tbody>
</table>

**Options for ports:**

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">protocol</td>
<td class="org-left">str</td>
<td class="org-left">'tcp', 'udp'</td>
<td class="org-left">#f</td>
<td class="org-left">'tcp'</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">port</td>
<td class="org-left">int</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#t</td>
<td class="org-left">None</td>
<td class="org-left">The port to export</td>
</tr>


<tr>
<td class="org-left">pot<sub>port</sub></td>
<td class="org-left">int</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">None</td>
<td class="org-left">dynamically allocated by default</td>
</tr>
</tbody>
</table>


### Examples


### `ansible-managed` Flavour

A freshly created pot is somewhat useless if you want to manage it with Ansible, because there is no Python installation, and no sudo.

    pkg install -y python3 sudo
    pkg clean -ayq

    - name: Install ansible-managed Flavour
      copy:
        dest: '/usr/local/etc/pot/flavours/ansible-managed.sh'
        src: 'ansible-managed.sh'
        mode: '0755'
      become: yes


<a id="org0ecc845"></a>

## Inventory


<a id="org071f6b5"></a>

## Pot Connection

This collection also provides a connection plugin to execute commands inside a Pot. Two variants are provided: one for local pots, and one for remote pots.


### Local Pots

<table id="org7a90ca5" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Variable</th>
<th scope="col" class="org-left">Type</th>
<th scope="col" class="org-left">Choices</th>
<th scope="col" class="org-left">Required?</th>
<th scope="col" class="org-left">Default</th>
<th scope="col" class="org-left">Info</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">ansible<sub>host</sub></td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">inventory<sub>hostname</sub></td>
<td class="org-left">Name of the jail</td>
</tr>


<tr>
<td class="org-left">ansible<sub>user</sub></td>
<td class="org-left">str</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">#f</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">User inside the jail to run as</td>
</tr>
</tbody>
</table>

1.  Examples


### Remote Pots

Connecting to remote pots works almost like the SSH connection plugin - it is an extension of it. The difference is that you have to specify the name of the pot, and of course tell Ansible to use the `zilti.pot.pot_remote` connection plugin. Here's an example inventory file:

    [jails]
    testpot1@192.168.121.13 ansible_connection=zilti.pot.pot_remote

Be aware that the connection plugin will need to use a `become` plugin to copy files into and out of the pot.


<a id="org2b02075"></a>

## Lookup Plugin

This lookup plugin is currently in a testing phase.


<a id="orgd149cdf"></a>

# Dependencies

Needs the `community.general` collection.


<a id="org93776f5"></a>

# Example Playbook

    - hosts: all
      become: yes
      remote_user: root
      roles:
      - role: zilti.pot.pot
        vars:
          pot:
    	enabled: true
    	vnet_enabled: true
    	zfs_root: tank/pot
    	extif: vtnet0
      tasks:
      - zilti.pot.pot_base:
          name: 13.1
          release: 13.1
    
      - zilti.pot.pot_fscomp:
          name: testfs
    
      - zilti.pot.pot_jail:
          name: testpot1
          base: 13.1
          type: single
          state: started
          mounts:
          - target: /opt
    	fscomp: testfs


<a id="org28db34f"></a>

# License

GPL3.0


<a id="org6d6357e"></a>

# Author Information

Daniel Ziltener, Code & Magic UG


<a id="orgd45118d"></a>

# Ansible Galaxy Metadata

    requires_ansible: ">=2.9"

    namespace: zilti
    name: pot
    version: 0.5.28
    
    authors:
      - Daniel Ziltener <dziltener@lyrion.ch>
    
    dependencies:
      community.general: "*"
    
    tags:
      - freebsd
      - jails
      - pot
    
    readme: README.md
    license: GPL-3.0-or-later
    description: Roles and modules for installing and using Pot
    
    repository: https://github.com/zilti/ansible-pot
    issues: https://github.com/zilti/ansible-pot/issues
    documentation: https://github.com/zilti/ansible-pot
    homepage: https://github.com/zilti/ansible-pot

    galaxy_info:
      author: Daniel Ziltener
      description: A role to manage Pot jails
      company: Code & Magic UG
    
      # If the issue tracker for your role is not on github, uncomment the
      # next line and provide a value
      # issue_tracker_url: http://example.com/issue/tracker
    
      # Choose a valid license ID from https://spdx.org - some suggested licenses:
      # - BSD-3-Clause (default)
      # - MIT
      # - GPL-2.0-or-later
      # - GPL-3.0-only
      # - Apache-2.0
      # - CC-BY-4.0
      license: GPL-3.0-or-later
    
      min_ansible_version: 2.9
    
      # If this a Container Enabled role, provide the minimum Ansible Container version.
      # min_ansible_container_version:
    
      #
      # Provide a list of supported platforms, and for each platform a list of versions.
      # If you don't wish to enumerate all versions for a particular platform, use 'all'.
      # To view available platforms and versions (or releases), visit:
      # https://galaxy.ansible.com/api/v1/platforms/
    
      platforms:
      - name: FreeBSD
        versions:
        - all
    
      galaxy_tags:
      - freebsd
      - jails
        # List tags for your role here, one per line. A tag is a keyword that describes
        # and categorizes the role. Users find roles by searching for tags. Be sure to
        # remove the '[]' above, if you add tags to this list.
        #
        # NOTE: A tag is limited to a single word comprised of alphanumeric characters.
        #       Maximum 20 tags per role.
    
    dependencies: []
      # List your role dependencies here, one per line. Be sure to remove the '[]' above,
      # if you add dependencies to this list.

