#!/usr/bin/env python3

import fatsecret as fs
import argparse
import yaml


def get_secrets(config):
    conn = fs.Fatsecret(**config)
    # Invoke OAuth for authorization and store the token and secret
    print("\n\n ------ Authorize your web function ------ \n\n")
    print("Follow this link and authorize your API key to access your data.")
    print(conn.get_authorize_url())
    config['session_token'] = conn.authenticate(input("\nPIN: "))
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Authorize and store FatSecret user token')
    parser.add_argument(
        'consumer_key', type=str, help='FatSecret API Consumer Key')
    parser.add_argument(
        'consumer_secret', type=str, help='FatSecret REST API Shared Secret')
    parser.add_argument(
        '--file',
        default='fs_credentials.yml',
        type=argparse.FileType('w'),
        help='credential storage file')
    args = parser.parse_args()
    config = {
        'consumer_key': args.consumer_key,
        'consumer_secret': args.consumer_secret
    }
    config = get_secrets(config)
    yaml.dump(config, args.file)
