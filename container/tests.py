from django.test import TestCase

from .models import Container

class ContainerModelTest(TestCase):

    def test_container_operation(self):
        default_ports = {
            'http': 80,
            'stream': 22
        }
        c = Container.create(name="Test", domain="test.lssc.club", ports=default_ports)
        c.activate()
        self.assertIs(c.activity, True)
        c.stop()
        self.assertIs(c.activity, False)
        c.destroy()
        self.assertIs(Container.objects.filter(name="Test").count(), 0)