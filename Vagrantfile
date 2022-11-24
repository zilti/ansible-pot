#!/usr/bin/env ruby

$script = <<-EOF
export ASSUME_ALWAYS_YES=YES
pkg install py39-ansible python3
rm -rf /usr/local/share/py39-ansible/collections/ansible_collections/zilti
ansible-galaxy collection install /vagrant/zilti/ -p /usr/local/share/py39-ansible/collections/
ansible-galaxy collection install community.general -p /usr/local/share/py39-ansible/collections/
EOF

Vagrant.configure("2") do |config|
  config.vm.box = "zilti/FreeBSD-13.1"
  config.vm.synced_folder ".", "/vagrant", type: "sshfs"
  config.vm.provision "shell", inline: $script
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "/vagrant/tests/test.yml"
    ansible.verbose = "-vvv"
  end
  config.vm.provider "libvirt" do |v|
    v.memory = 2048
  end
end
