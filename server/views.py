from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from server.decorators import basic_auth
from server.models import Record
from server import utils

@basic_auth
def index(request, ip):
    try:
        protocol, ip_address = utils.get_ip_address(ip)
    except ValueError:
        return HttpResponseBadRequest('Invalid IP', content_type='text/plain')

    if not ip_address.is_global or ip_address.is_multicast:
        return HttpResponse('Forbidden IP', status=422, content_type='text/plain')

    record = Record(
        client = request.user,
        protocol = protocol,
        remote_ip = request.META['REMOTE_ADDR'],
        update_ip = str(ip_address)
    )

    record.save()

    utils.update_cloudflare(request.user, record)

    return HttpResponse(ip, content_type='text/plain')

@basic_auth
def traefik_forwardedauth_acmeproxy(request):
    # Source IP-Address set by Traefik ForwardAuth
    source_ip = request.headers.get('X-Forwarded-For')

    # Check if the authenticated client (user) has an update record that matches source IP
    try:
        record = request.user.latest_record(source_ip)
    except (Record.DoesNotExist, ValidationError):
        record = None

    # Return 202 Accepted to authorize ACME request
    if record is not None:
        return HttpResponse(status = 202, content_type='text/plain')

    # Return 401 Unauthorized to reject the request
    return HttpResponse(status = 401, content_type='text/plain')