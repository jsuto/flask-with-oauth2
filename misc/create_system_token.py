#!/usr/bin/python3

from authlib.jose import JsonWebSignature
import json
import os
import uuid

header = {'alg': 'HS256'}

system_token = str(uuid.uuid4())
payload = json.dumps({'system_token': system_token, 'customerid': 'fictive'})
secret = os.getenv("CLIENT_SECRET", "aaaa")

jws = JsonWebSignature()
jwt_token = jws.serialize_compact(header, payload, secret)

print(f"system_token: {system_token}\nJWT token: {jwt_token.decode('utf-8')}")
