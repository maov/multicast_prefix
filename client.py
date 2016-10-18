#!/usr/bin/env python
import socket
import sys
import common as cc
import time
import logging
import hashlib

LOCAL_IP6="fdee:f345:543f::3/64"
PREFIX="fdee:f345:543f:{0}:{1}::/80"


def local_prefix() :
    #use hashlib to generate prefix, and hope for no clash
    prefix_seed = hashlib.md5(hostname.encode("utf-8")).hexdigest()[0:8]
    return PREFIX.format(prefix_seed[0:4], prefix_seed[4:8])


while True:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    hostname = socket.gethostname()
    msg = '{0};{1};{2}'.format(hostname,LOCAL_IP6, local_prefix())
    print('Sending multicast {0}'.format(msg.encode('utf-8')))
    sock.sendto(msg.encode('utf-8'), ('', cc.PORT))
    time.sleep(6)
