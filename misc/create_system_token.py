#!/usr/bin/python3
"""
Create a jwt token
"""

import json
import os
import uuid
from authlib.jose import JsonWebSignature

header = {'alg': 'HS256'}

SYSTEM_TOKEN = str(uuid.uuid4())
payload = json.dumps({'SYSTEM_TOKEN': SYSTEM_TOKEN, 'customerid': 'fictive'})
secret = os.getenv("CLIENT_SECRET", "aaaa")

jws = JsonWebSignature()
jwt_token = jws.serialize_compact(header, payload, secret)

print(f"SYSTEM_TOKEN: {SYSTEM_TOKEN}\nJWT token: {jwt_token.decode('utf-8')}")
