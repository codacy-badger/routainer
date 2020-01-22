# routainer
Control panel for LXC container and NGINX proxy

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/lssc/routainer/Python%20application)
![GitHub](https://img.shields.io/github/license/lssc/routainer)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/lssc/routainer)

## Installation
This project is intended to run on a clean installed CentOS 8.

1. Enable EPEL repository for lxc
```shell
dnf install epel-release
```

2. Install Python3, NGINX and LXC
```shell
dnf install python3 nginx lxc
```

3. Enable and start the services
```shell
systemctl start lxc
systemctl start nginx
```

4. To be continue...
