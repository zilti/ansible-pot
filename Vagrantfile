#!/usr/bin/env ruby

$script = <<-EOF
export ASSUME_ALWAYS_YES=YES
pkg install py39-ansible
EOF

Vagrant.configure("2") do |config|
  config.vm.box = "zilti/FreeBSD-13.1"
  config.vm.provision "shell", inline: $script
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "tests/test.yml"
  end
end
