#!/usr/bin/python3

import argparse
import os
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jwt-token", type=str, help="The jwt token", required=True)
    parser.add_argument("-u", "--uri", type=str, default="http://localhost:5000", help="The backend uri", required=True)
    args = parser.parse_args()

    headers = {
        "Authorization": "Bearer %s" % args.jwt_token
    }

    response = requests.request("GET", args.uri, headers=headers)

    print(response.text)

if __name__ == "__main__":
    main()
