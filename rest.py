import json
from flask import Flask

with open('lenovo_computers.json', 'r') as f:
    data = json.load(f)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.get("/")
def hello_world():
    return data