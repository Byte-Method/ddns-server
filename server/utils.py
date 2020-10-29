import CloudFlare as Cloudflare

from ipaddress import ip_address, IPv4Address, IPv6Address
from .models import Record

def get_ip_address(value):
    obj = ip_address(value)

    if isinstance(obj, IPv4Address):
        protocol = Record.PROTOCOL_IPV4
    
    if isinstance(obj, IPv6Address):
        protocol = Record.PROTOCOL_IPV6

    return protocol, obj

def update_cloudflare(client, ddns_record):
    cf = Cloudflare.CloudFlare()

    dns_records = cf.zones.dns_records.get(client.cf_zone)

    for dns_record in dns_records:
        if dns_record['name'] == client.domain:
            if (dns_record['type'] == 'A' and ddns_record.is_ipv4()) \
                or (dns_record['type'] == 'AAAA' and ddns_record.is_ipv6()):
                cf.zones.dns_records.patch(client.cf_zone, dns_record['id'], data={
                    'content': ddns_record.update_ip
                })
