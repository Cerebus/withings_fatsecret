from flask import Flask, request
import fatsecret as fs
import yaml

app = Flask(__name__)

lb_to_kg = 0.45359237

with open('credentials.yml') as f:
        config = yaml.load(f)

@app.route('/', methods=['POST'])
def api_root():
    conn = fs.Fatsecret(
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        session_token=(config['user_token'], config['user_secret'])
        )
    return str(conn.weight_update(request.get_json()['weightkg']))


