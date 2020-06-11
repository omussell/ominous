# Ominous

# Problem statement

Lots of nodes using NGINX as a proxy to upstream application servers. Need a way of gracefully changing the config of NGINX when a new application server is deployed. Also, just generally a way of centrally managing NGINX config without relying on configuration management systems. Config management system are great but the modules/formulae/plugins in them to manage NGINX are complicated and its often easier to just use the built in file/service resources.

Likewise, NGINX is used as a API gateway / load balancer / TLS terminator. We need to use a central place to configure all these nodes.

[Crossplane](https://github.com/nginxinc/crossplane) is a python package written by NGINX which converts the NGINX config into JSON format and vice versa. This makes it possible to store the NGINX config in a database for example, and means the JSON can be sent as part of a normal HTTP request. 

So the idea is to have an  app with a database which serves as the storage for the NGINX configs across the infrastructure. The configs could be amended using a frontend interface. When a config is modified, the app would send an API request to the node containing the new NGINX config. There would be an agent on the node which would receive this API request, convert the NGINX config into the correct files on the node, and reload NGINX.

A further extension of this is to also be able to control NGINX Unit. Unit stores its config inside a HTTP API, so changes to the config are done by sending JSON content in a HTTP request. We could extend the app to also include configuring NGINX Unit. Unit is also usually protected by NGINX anyway, in that requests to the Unit control socket are proxied via NGINX.


# ominous

- fastapi
- sqlalchemy - ORM
- alembic - db migrations

# ominous-client

- fastapi
- sqlite - db
- sqlalchemy - ORM
- alembic - db migrations



# Example crossplane

```
import crossplane
payload = crossplane.parse('nginx.conf')
# The whole parsed config
print(payload['config'])
# The first file in the config
print(payload['config'][0])
# The actual config of the first file
print(payload['config'][0]['parsed'])
# Print the proper formatted version
crossplane.build(payload['config'][0]['parsed'])
```



- Get the NGINX configs
- should be able to use query strings to get specific config files

- if putting the new config in place causes NGINX -t to fail, revert to previous config? 
- but crossplane should pick up any errors
- see https://github.com/nginxinc/crossplane#crossplane-parse-advanced
- should use this, run crossplane with checks prior to applying the config
- the node itself should check though in case there is node specific config. Then the errors can be returned to the master
 
- create CI / build steps using invoke
 
- allow jinja2 variables in config file, filled in by app specific attributes set in the web interface? then config files can be templated and the same for multiple servers, except with app specific variables.
 



- server is running NGINX.
- get current config
- post new config
- should we be able to post individual files?
- or update individual files?
- as URL param maybe?
- configs need to be associated with a particular server / nginx instance
- needs to also be able to handle nginx unit 
- what about unit tests?
- integration tests?
- fabric model, nginx proxy, nginx in container + unit in container

- how to handle running this app? nginx + nginx unit configs? secondary profile or could it be considered the bootstrap config?

- if ominous-client is open to the internet, anyone could post to it with a nginx config, then it would just overwrite everything. Need to restrict by IP. Maybe we could generate a token or API key per NGINX instance too?
- cant use the NGINX API key way because its a catch 22, how to pass the key without using ominous? unless its a bootstrapping thing? initial setup is fine???
- not query params because NGINX cant route on that
- nginx_instance_url/ominous/containers/container1/unit
- proxy to container1
- rewrite to be normal URL so om-c in jail understands it
-         location /ominous/containers/container1 {
-            proxy_pass http://container1;
-            rewrite ^(/ominous)(/containers/container1) $1  break;
-        }
 
- for generating tokens:
- import secrets
- secrets.token_urlsafe(256)
- https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe

- Use minica for certificates?

- should client use sqlite to store the config?
- then the config will persist if NGINX is uninstalled or otherwise broken
- you could just reapply the config rather than have to rebuild it
- but would then need to check if applied config matches what is in the database...
- regular task to check?
- or ominous sends health check to instances, run function to compare what is on the server to what is in the database
- if different, flag it for remediation
- check out background tasks on fastapi, maybe have it send health check request to see if server is still up, and the background task compiles the running config and compares it to the stored config

- crossplane splits up config into Config and Directive objects. 
- use a combination of pydantic models and dataclasses to store these objects
- then those objects can be mapped to fields in the database
- since they are split up, they could be modified directly e.g. via url params
- unsure whether storing values in json fields is necessary, if the above work on objects is done

- interactions with api via fastapi should be async
- interactions with db should be async

- integration tests using tavern
- unit tests using hypothesis


# Bootstrapping

Does the ominous-client need nginx  to run properly?
ominous-client needs at least supervisor
if so, nginx is already installed and running, and contains some config already.
Should we be using HTTPS between client and ominous?
use token to authenticate initial cert creation then rotate token and cert?
should this stuff be in separate app to client so that it can be modified or otherwise not used?
probs not, should be secure by default

just get app working without any auth first... 



- Assume there is a server with ominous running. It has no config for the new node.
- The new node is created and the ominous-client package is installed.
  - NGINX is installed by some separate process. 
- ominous-client generates a new API token and checks in to ominous. Provides the hostname and API token.
  - This initial token is temporary but allows the client and master to authenticate.
- ominous creates new node in the database, and records the API token.
  - If possible, the API token field should be encrypted.
- ominous-client pulls the generic config from ominous which includes the API token and applies the NGINX config.
  - This is so that ominous can send HTTPS requests to ominous-client via the NGINX proxy terminating TLS. 
- ominous creates a new API token.
- The config for the new node is created.
- The config is sent to the new node.
- ominous-client gets the config and applies it.



