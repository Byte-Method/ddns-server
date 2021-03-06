import uuid
from string import ascii_letters, digits

from django.db import models
from django.utils.crypto import get_random_string


def get_random_key():
	return get_random_string(length=32, allowed_chars=ascii_letters+digits)

class Client(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    key = models.CharField(max_length=32, default=get_random_key)
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    domain = models.CharField(max_length=253)
    cf_zone = models.CharField(max_length=255)

    def latest_record(self, filter_ip = None):
        if filter_ip:
            return Record.objects.filter(client=self, update_ip = filter_ip).latest('updated_on')
        
        return Record.objects.filter(client=self).latest('updated_on')
    
    def __str__(self):
        return f'{self.name} ({self.uuid})'


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

    def __str__(self):
        return self.update_ip
