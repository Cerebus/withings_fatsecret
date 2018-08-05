import fatsecret as fs
import yaml
import boto3
from botocore.exceptions import ClientError

lb_to_kg = 0.45359237

with open('fatsecret.yml') as f:
    config = yaml.load(f)


def update_fatsecret(weight_kg):
    conn = fs.Fatsecret(
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        session_token=(config['user_token'], config['user_secret']))
    return conn.weight_update(weight_kg)


# Use this code snippet in your app.
# If you need more information about configurations or implementing
# the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/


def get_secret():
    secret_name = "Fatsecret_API_credential"
    endpoint_url = "https://secretsmanager.us-west-2.amazonaws.com"
    region_name = "us-west-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
    else:
        # Decrypted secret using the associated KMS CMK
        # Depending on whether the secret was a string or binary, one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']

        # Your code goes here.
