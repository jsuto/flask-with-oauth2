#!/usr/bin/python3
"""
Test if the flask app can be accessed with jwt token
"""

import argparse
import requests


def main():
    """
    Send request to the flask app
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jwt-token", type=str, help="The jwt token",
                        required=True)
    parser.add_argument("-u", "--uri", type=str, default="http://localhost:5000",
                        help="The backend uri", required=True)
    args = parser.parse_args()

    headers = {
        "Authorization": f"Bearer {args.jwt_token}"
    }

    response = requests.request("GET", args.uri, headers=headers, timeout=10)

    print(response.text)


if __name__ == "__main__":
    main()
