# FLASK_APP=ominous-agent.py flask run
# curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/nginx_config -d "`crossplane parse nginx.conf`"
from flask import Flask
from flask import json
from flask import request
import crossplane
import subprocess

app = Flask(__name__)

# function to load nginx config files as json using crossplane. optional parameter of specific config files
# maybe this should be in another app since we'll use it in multiple places?

@app.route('/nginx_config', methods = ['POST'])
def update_nginx():
    with open('nginx.json', 'w') as outfile:
        writeme = json.dumps(request.json)
        #outfile.write(json.dumps(request.json))
        outfile.write(writeme)
        subprocess.run(["crossplane", "build", "nginx.json", "-f",])
        return "it bloody well worked"

# Get the NGINX configs
# should be able to use query strings to get specific config files
@app.route('/nginx_config', methods = ['GET'])
def update_nginx():
    with open('nginx.json', 'w') as outfile:
        writeme = json.dumps(request.json)
        #outfile.write(json.dumps(request.json))
        outfile.write(writeme)
        subprocess.run(["crossplane", "build", "nginx.json", "-f",])
        return "it bloody well worked"


# subprocess.run(["crossplane", "build", "nginx.json", "-f",])
