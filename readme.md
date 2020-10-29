# DDNS Server

This is a simple Django project that exposes an API for configured clients to send IP address updates to.

# Background

This project was created to keep track of remote pfSense firewalls, without storing sensitive Cloudflare API keys on each appliance.

pfSense comes with a built-in dynamic DNS client that supports custom URLs and HTTP Basic authentication.

# Configuration

Login to Django Admin, and create a new **Client**. The UUID will be used as the *Username* and the *Key* will be the password. Set *Domain* to the FQDN of the domain to update, and *CF Zone* to the Cloudflare zone ID of the domain.

The Cloudflare API token can be provided through the `CF_API_KEY` environment variable.

## pfSense

Create a new Dynamic DNS client, choose the `Custom` **Service Type** and configure the client:

| Field        | Value                                      |
|--------------|--------------------------------------------|
| Username     | *client UUID*                              |
| Password     | *client key*                               |
| Update URL   | `https://ddns.example.com/api/update/%IP%` |
| Result Match | `%IP%`                                     |

The same steps can be repeated for an IPv6 interface. The IP version will automatically be detected.

# To Do

* Hash the keys, instead of using plaintext