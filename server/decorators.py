import base64

from django.http import HttpResponse
from django.conf import settings

from server.auth.backends import DDNSClientBackend

def basic_auth(view):
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uuid, key = base64.b64decode(auth[1]).decode("utf8").split(':', 1)

                    backend = DDNSClientBackend()

                    client = backend.authenticate(request, uuid=uuid, key=key)
                    
                    if client is not None and client.is_active:
                        request.user = client
                        return view(request, *args, **kwargs)

        response = HttpResponse(status = 401, content_type='text/plain')
        response['WWW-Authenticate'] = 'Basic realm="{}"'.format('DDNS')
        return response
    return wrap