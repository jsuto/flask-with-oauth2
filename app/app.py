from authlib.jose import jwt, JsonWebSignature, errors
from flask import Flask, session, redirect, request, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
import azure
import json
import logging
import os
import requests
import sys
import uuid

CLIENT_ID = os.getenv("CLIENT_ID", "aaaa")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "aaaa")
CALLBACK_URI = os.getenv("CALLBACK_URI", "http://localhost:5000/auth")
LISTEN_ADDRESS = os.getenv("LISTEN_ADDRESS", "0.0.0.0")
LISTEN_PORT = os.getenv("LISTEN_PORT", 5000)
BEHIND_PROXY = os.getenv("BEHIND_PROXY", 0)

app = Flask(__name__)


def get_client_ip():
    return request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

def check_system_token(headers, secret):
    if 'Authorization' in headers and headers['Authorization'].startswith("Bearer"):
        pos = headers['Authorization'].index("eyJ")
        token = headers['Authorization'][pos:]
        jws = JsonWebSignature()

        try:
            payload = jws.deserialize_compact(token, secret)
            payload = json.loads(payload['payload'].decode())

            if 'system_token' in payload:
                app.logger.info('system token %s from %s', payload['system_token'], get_client_ip())
                return payload['system_token']
        except errors.BadSignatureError:
            app.logger.error('Invalid system token')

    return None

@app.route('/')
def homepage():
    system_token = check_system_token(request.headers, CLIENT_SECRET)
    user = session.get('user')
    return render_template('index.html', user=user, system_token=system_token)

@app.route('/login')
def login():
    state = str(uuid.uuid4())
    session['state'] = state
    redirect_uri = "%s?client_id=%s&redirect_uri=%s&state=%s&scope=openid profile email&response_type=code" % \
                   (azure.AUTHORIZATION_ENDPOINT, CLIENT_ID, CALLBACK_URI, state)

    return redirect(redirect_uri)

@app.route('/auth')
def auth():
    code = request.args.get('code')
    state_from_request = request.args.get('state')

    state = session['state']

    if state != state_from_request:
        return "Invalid session from request", 403

    auth_data = "grant_type=authorization_code&client_id=%s&client_secret=%s&redirect_uri=%s&code=%s" % \
                (CLIENT_ID, CLIENT_SECRET, CALLBACK_URI, code)

    oauth = azure.AZURE()

    oauth.get_id_token(auth_data)
    if oauth.error:
        return oauth.error, 403

    oauth.parse_id_token()

    oauth.get_public_key()
    if oauth.error:
        return oauth.error, 403

    claims = jwt.decode(oauth.id_token, oauth.pubkey_str)
    if 'email' not in claims:
        return "Cannot identify user email", 403

    session['user'] = claims

    app.logger.info('%s logged in from %s', session['user']['email'], get_client_ip())

    return redirect('/')

@app.route('/logout')
def logout():
    if 'user' in session:
        app.logger.info('%s logged out', session['user']['email'])

    session.pop('user', None)
    session.pop('state', None)

    return redirect('/')

@app.route('/status')
def version():
    return "ok"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format = '%(message)s')

    if BEHIND_PROXY:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    app.secret_key = str(int.from_bytes(os.urandom(20), sys.byteorder))
    app.run(host=LISTEN_ADDRESS, port=LISTEN_PORT)
