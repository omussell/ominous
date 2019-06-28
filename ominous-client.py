# FLASK_APP=ominous-agent.py flask run
# curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/update_nginx -d "`crossplane parse nginx.conf`"
from flask import Flask
from flask import json
from flask import request
import crossplane
import subprocess

app = Flask(__name__)

@app.route('/update_nginx', methods = ['POST'])
def update_nginx():
    with open('nginx.json', 'w') as outfile:
        writeme = json.dumps(request.json)
        #outfile.write(json.dumps(request.json))
        outfile.write(writeme)
        subprocess.run(["crossplane", "build", "nginx.json", "-f",])
        return "it bloody well worked"


# subprocess.run(["crossplane", "build", "nginx.json", "-f",])
