#!/bin/sh

# Enable EPEL Repository
dnf install -y epel-release
# Install LXC
dnf install -y lxc lxc-templates python3-lxc
# Install NGINX
dnf install -y nginx
# Install pip3
dnf install -y python3-pip

# Install Django
python3 -m pip install --upgrade pip
pip3 install django

# Configure LXC
echo 'root:100000:65536' >> /etc/subuid
echo 'root:100000:65536' >> /etc/subgid

echo 'lxc.idmap = u 0 100000 65536' >> /etc/lxc/default.conf
echo 'lxc.idmap = g 0 100000 65536' >> /etc/lxc/default.conf

echo 'Reboot required'