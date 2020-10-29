from django.core.exceptions import ValidationError
from django.utils.crypto import constant_time_compare
from django.contrib.auth.backends import BaseBackend

from server.models import Client

class DDNSClientBackend(BaseBackend):
    def authenticate(self, request, uuid=None, key=None):
        try:
            client = Client.objects.get(uuid=uuid)
        except (Client.DoesNotExist, ValidationError):
            client = None
        
        if client is not None and constant_time_compare(key, client.key):
            return client