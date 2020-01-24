from django.db import models

from router.models import Router
import lxc


class Container(models.Model):
    name = models.CharField(max_length=16)
    domain = models.CharField(max_length=100)
    activity = models.BooleanField()
    exposed_port = models.CharField(max_length=200)

    @classmethod
    def create(cls, name, domain, ports):
        # Setup the container object
        c = lxc.Container(name)
        # Create the container rootfs
        c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                    "release": "bionic",
                                                    "arch": "amd64"})
        # Install OpenSSH Server
        c.attach_wait(lxc.attach_run_command,
                      ["apt-get", "update"])
        c.attach_wait(lxc.attach_run_command,
                      ["apt-get", "upgrade", "-y"])
        c.attach_wait(lxc.attach_run_command,
                      ["apt-get", "install", "openssh-server", "-y"])

        # Create container object in database
        container = cls(name=name, domain=domain,
                        activity=False, exposed_port=ports)
        # add rules to router
        for p in ports['http']:
            container.addRoute(p, 'http')
        for p in ports['stream']:
            container.addRoute(p, 'stream')

        return container

    def destroy(self):
        Router.objects.filter(container_name=self.name).delete()
        c = lxc.Container(self.name)
        c.destroy()
        self.delete()

    def activate(self):
        c = lxc.Container(self.name)
        c.start()
        self.activity = (
            c.state == "STARTING" or c.state == "RUNNING")
        self.save()

    def deactivate(self):
        c = lxc.Container(self.name)
        c.stop()
        self.activity = (
            c.state == "STOPPING" or c.state == "STOPPED")
        self.save()

    def addRoute(self, port, ptype):
        rule = Router.create(self.name, port, ptype)
        rule.save()
