#!/usr/bin/python3 -u

import jwt
import os
import fileinput

fd = open("/tmp/check.log", "a")

BEARER = "Bearer%20"

for line in fileinput.input():
    fd.write(line)
    fd.flush()
    if not line.startswith(BEARER):
        print("ERR")
        continue
    token = line[len(BEARER):-1]
    try:
        payload = jwt.decode(token, verify=False)
        print("OK")
    except jwt.DecodeError:
        print("ERR")
