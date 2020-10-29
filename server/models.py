import uuid
from django.db import models

class Client(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    key = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    domain = models.CharField(max_length=253)
    cf_zone = models.CharField(max_length=255)


class Record(models.Model):
    PROTOCOL_IPV4 = 'ipv4'
    PROTOCOL_IPV6 = 'ipv6'

    PROTOCOL_CHOICES = [
        (PROTOCOL_IPV4, 'IPv4'),
        (PROTOCOL_IPV6, 'IPv6'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=4, choices=PROTOCOL_CHOICES)
    remote_ip = models.GenericIPAddressField()
    update_ip = models.GenericIPAddressField()
    updated_on = models.DateTimeField(auto_now_add=True)

    def is_ipv4(self):
        return self.protocol == self.PROTOCOL_IPV4
    
    def is_ipv6(self):
        return self.protocol == self.PROTOCOL_IPV6