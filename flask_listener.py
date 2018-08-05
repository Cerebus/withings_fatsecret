from flask import Flask, request
import fatsecret as fs
import yaml

app = Flask(__name__)

with open('fs_credentials.yml') as f:
    config = yaml.load(f)


@app.route('/', methods=['POST'])
def api_root():
    conn = fs.Fatsecret(**config)
    return str(conn.weight_update(request.get_json()['weightkg']))
