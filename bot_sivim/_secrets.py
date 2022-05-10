#!/usr/bin/env python3

import json

def get_secrets(*args):
	with open('secrets.json') as f:
		secrets = json.load(f)

		return [secrets[key] for key in args]

def get_secret(secret):
	with open('secrets.json') as f:
		secrets = json.load(f)

		return secrets[secret]
