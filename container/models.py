from django.db import models

from router.models import Router
import logging
import lxc

logger = logging.getLogger(__name__)


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
        if not c.create("ubuntu", lxc.LXC_CREATE_QUIET):
            logger.error("Failed to create the container rootfs")
            raise Exception("Failed to create the container rootfs")
        else:
            logger.debug("Container created")

        # Create container record in database
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
        if not c.destroy():
            logger.error("Failed to destroy the container")
            raise Exception("Failed to destroy the container")
        else:
            self.delete()

    def activate(self):
        c = lxc.Container(self.name)
        if not c.start():
            logger.error("Failed to start the container")
            raise Exception("Failed to start the container")
        else:
            logger.debug("Container started")
            c.state = True
        self.save()

    def deactivate(self):
        c = lxc.Container(self.name)
        if not c.shutdown(30):
            logger.error(
                "Failed to cleanly shutdown the container, forcing...")
            if not c.stop():
                logger.error("Failed to kill the container")
                raise Exception("Failed to kill the container")
            else:
                logger.debug("Container killed")
                c.state = False
        else:
            logger.debug("Container stopped")
            c.state = False
        self.save()

    def addRoute(self, port, ptype):
        rule = Router.create(self.name, port, ptype)
        rule.save()
