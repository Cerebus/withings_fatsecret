from flask import Flask, request
import fatsecret as fs
import boto3
import json

app = Flask(__name__)

secret_manager = boto3.client('secretsmanager')
fatsecret_cred = json.loads(secret_manager.get_secret_value(
    SecretId='Fatsecret_API_credential')['SecretString'])
user_cred = json.loads(secret_manager.get_secret_value(
    SecretId='Fatsecret_cerebus_credential')['SecretString'])

config = {
    'consumer_key': fatsecret_cred['fatsecret_consumer_key'],
    'consumer_secret': fatsecret_cred['fatsecret_consumer_secret'],
    'session_token': (user_cred['cerebus_token'], user_cred['cerebus_secret'])
}


@app.route('/', methods=['POST'])
def api_root():
    conn = fs.Fatsecret(**config)
    return str(conn.weight_update(request.get_json()['weightkg']))
