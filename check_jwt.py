#!/usr/local/bin/python3 -u

import fileinput
import argparse
import jwt

BEARER = "Bearer%20"

def parse_args():
    parser = argparse.ArgumentParser(description='check jwt token')
    parser.add_argument('--pub-key', default='/etc/squid3/jwt-pub-key.pem')
    parser.add_argument('--no-verify', action='store_true', default=False)
    parser.add_argument('--no-verify-aud', action='store_true', default=False)
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.no_verify:
        with open(args.pub_key, "r") as f:  #pylint: disable=invalid-name
            pub_key = str.encode("".join(f.readlines()))
    else:
        pub_key = None

    for line in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
        if not line.startswith(BEARER):
            print("ERR")
            continue
        token = line[len(BEARER):-1]
        try:
            payload = jwt.decode(token, pub_key,   #pylint: disable=unused-variable
                                 verify=(not args.no_verify),
                                 options={"verify_aud": (not args.no_verify_aud)},
                                 algorithms="RS256")
            print("OK")
        except jwt.exceptions.InvalidTokenError:
            print("ERR")


if __name__ == "__main__":
    main()
