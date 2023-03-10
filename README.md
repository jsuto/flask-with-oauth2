# flask-with-oauth2



## Getting started

Register a multitenant web app in Azure AD.

You need to export the following env variables:
- CLIENT_ID
- CLIENT_SECRET
- CALLBACK_URI

## Build docker image

```
docker build -t sutoj/flaskapp:0.1 .
```

Put the env variables mentioned above to env.txt

```
docker run -d --name testapp --env-file env.txt -p 5000:5000 sutoj/flaskapp:0.1
```

## Kubernetes deployment

See the manifests in the kubernetes directory.
Note that you need to create a kubernetes secret for the CLIENT_SECRET value.

## Utilities

### create_system_token.py

Create a system token and a JWT token encrypted by CLIENT_SECRET

### test_backend_with_system_token.py

Test the app accessibility using a JWT token
