#!/bin/sh

# Enable EPEL Repository
dnf install -y epel-release
# Install LXC
dnf install -y lxc lxc-templates python3-lxc
# Install pip3
dnf install -y python3-pip

# Install Django
python3 -m pip install --upgrade pip
pip3 install django