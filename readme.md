# DDNS Server

This is a simple Django project that exposes an API for configured clients to send IP address updates to.

# Background

This project was created to keep track of remote pfSense firewalls, without storing sensitive Cloudflare API keys on each appliance.

pfSense comes with a built-in dynamic DNS client that supports custom URLs and HTTP Basic authentication.

# Install

To use the admin area, the static files must be collected, and the database initialized.

E.g., if you're using the provided `docker-compose.yml`:

```
docker-compose exec ddns-server sh -c "python manage.py collectstatic && python manage.py makemigrations && python manage.py migrate"
```

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

## Sample NGINX Config
```nginx
upstream app {
	server ddns-server:8000;
}

server {
	listen 80;

	root /var/www/html;

	location = /favicon.ico { access_log off; log_not_found off; }
	
	location / {
		try_files $uri @proxy_app;
	}

	location @proxy_app {
		proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header Host              $http_host;

		proxy_redirect  off;
		proxy_buffering off;

		proxy_pass http://app;
	}
}
```

# To Do

* Hash the keys, instead of using plaintext