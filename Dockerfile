FROM alpine:3.8

RUN apk add --no-cache squid python3 py3-jwt

ADD check_jwt.py squid.conf /etc/squid/

ENTRYPOINT ["/usr/sbin/squid", "-N", "-d 1"]
