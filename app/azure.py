import base64
import json
import requests
import util
from OpenSSL import crypto

OPENID_CONF_URL = "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
AUTHORIZATION_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
KEYS_ENDPOINT = "https://login.microsoftonline.com/common/discovery/v2.0/keys"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

class AZURE:
    def __init__(self):
        self.pubkey_str = None
        self.id_token = None
        self.access_token = None
        self.header = None
        self.payload = None
        self.error = None

    def get_public_key(self):
        self.error = "No matching certificate found"

        resp = requests.get(KEYS_ENDPOINT)
        r = resp.json()

        if 'keys' in r:
            keys = r['keys']
            for i in range(len(keys)):
                if keys[i]['kid'] == self.header['kid']:
                    cert_str = f"-----BEGIN CERTIFICATE-----\n{keys[i]['x5c'][0]}\n-----END CERTIFICATE-----\n"
                    cert_obj = crypto.load_certificate(crypto.FILETYPE_PEM, cert_str)
                    pubkey_obj = cert_obj.get_pubkey()
                    self.pubkey_str = crypto.dump_publickey(crypto.FILETYPE_PEM, pubkey_obj)
                    self.error = None
                    break

    def get_id_token(self, auth_data):
        resp = requests.post(TOKEN_ENDPOINT, data=auth_data)
        r = resp.json()

        if 'error' in r:
            self.error = r['error']

        if 'id_token' in r:
            self.id_token = r['id_token']
        else:
            self.error = "No id_token in response"

        if 'access_token' in r:
            self.access_token = r['access_token']
        else:
            self.error = "No access_token in response"

    def parse_id_token(self):
        (headerb64, payloadb64, signature) = self.id_token.split(".")

        self.header = json.loads(base64.b64decode(util.fix_base64_padding(headerb64)))
        self.payload = json.loads(base64.b64decode(util.fix_base64_padding(payloadb64)))
