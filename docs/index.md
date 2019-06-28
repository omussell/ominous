# Ominous

# Problem statement

Lots of nodes using NGINX as a proxy to upstream application servers. Need a way of gracefully changing the config of NGINX when a new application server is deployed. Also, just generally a way of centrally managing NGINX config without relying on configuration management systems. Config management system are great but the modules/formulae/plugins in them to manage NGINX are complicated and its often easier to just use the built in file/service resources.

Likewise, NGINX is used as a API gateway / load balancer / TLS terminator. We need to use a central place to configure all these nodes.

[Crossplane](https://github.com/nginxinc/crossplane) is a python package written by NGINX which converts the NGINX config into JSON format. This makes it possible to store the NGINX config in a database for example, and means the JSON can be sent as part of a normal HTTP request. 

So the idea is to have a Django app with a database which serves as the storage for the NGINX configs across the infrastructure. The configs could be amended using a frontend interface. When a config is modified, the app would send an API request to the node containing the new NGINX config. There would be an agent on the node which would receive this API request, convert the NGINX config into the correct files on the node, and reload NGINX.

A further extension of this is to also be able to control NGINX Unit. Unit stores its config inside a HTTP API, so changes to the config are done by sending JSON content in a HTTP request. We could extend the Django app to also include configuring NGINX Unit. Unit is also usually protected by NGINX anyway, in that requests to the Unit control socket are proxied via NGINX.


# ominous-master

Django

# ominous-node

Django or flask?



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



