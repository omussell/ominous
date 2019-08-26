# FLASK_APP=ominous-agent.py flask run
# curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/nginx_config -d "`crossplane parse nginx.conf`"
from flask import Flask
from flask import json
from flask import request
import crossplane # type: ignore
import subprocess

app = Flask(__name__)

# below works. file['file'] is the filename
# file['parsed'] is an array of directives, which is the input that crossplane.build expects
# returns a single string that contains the entire NGINX config
#>>> for file in payload['config']:
#...     print(file['file'])
#...     crossplane.build(file['parsed'])

# function to load nginx config files as json using crossplane. optional parameter of specific config files
# maybe this should be in another app since we'll use it in multiple places?

@app.route('/nginx_config', methods = ['POST'])
def update_nginx():
    payload = json.dumps(request.json)
    for config_file in payload['config']:
        with open(config_file['file'], 'w') as cf:
            file_contents = crossplane.build(config_file['parsed'])
            cf.write(file_contents)
            return "it bloody well worked"

## Get the NGINX configs
## should be able to use query strings to get specific config files
#@app.route('/nginx_config', methods = ['GET'])
#def update_nginx():
#    with open('nginx.json', 'w') as outfile:
#        writeme = json.dumps(request.json)
#        #outfile.write(json.dumps(request.json))
#        outfile.write(writeme)
#        subprocess.run(["crossplane", "build", "nginx.json", "-f",])
#        return "it bloody well worked"




# server is running NGINX.
# get current config
# post new config
# should we be able to post individual files?
# or update individual files?
# as URL param maybe?
# configs need to be associated with a particular server / nginx instance
# needs to also be able to handle nginx unit 
# what about unit tests?
# integration tests?
# fabric model, nginx proxy, nginx in container + unit in container
 
# how to handle running this app? nginx + nginx unit configs? secondary profile or could it be considered the bootstrap config?

# if ominous-client is open to the internet, anyone could post to it with a nginx config, then it would just overwrite everything. Need to restrict by IP. Maybe we could generate a token or API key per NGINX instance too?
# cant use the NGINX API key way because its a catch 22, how to pass the key without using ominous? unless its a bootstrapping thing? initial setup is fine???
# not query params because NGINX cant route on that
# nginx_instance_url/ominous/containers/container1/unit
# proxy to container1
# rewrite to be normal URL so om-c in jail understands it
#         location /ominous/containers/container1 {
#            proxy_pass http://container1;
#            rewrite ^(/ominous)(/containers/container1) $1  break;
#        }
