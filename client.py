#!/usr/bin/env python
import socket
import sys
import common as cc
import time
import logging
import hashlib

LOCAL_IP6="{0}::1/64".format(cc.COMMON_PREFIX)
TEST_IP6="{0}::3/64".format(cc.COMMON_PREFIX)
PREFIX= "{0}:{1}:{2}::/80"


def local_prefix() :
    #use hashlib to generate prefix, and hope for no clash
    prefix_seed = hashlib.md5(hostname.encode("utf-8")).hexdigest()[0:8]
    return PREFIX.format(cc.COMMON_PREFIX,prefix_seed[0:4], prefix_seed[4:8])


while True:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    hostname = socket.gethostname()
    msg = '{0};{1};{2}'.format(hostname,LOCAL_IP6, local_prefix())
    print('Sending multicast {0}'.format(msg.encode('utf-8')))
    print(TEST_IP6)
    sock.sendto(msg.encode('utf-8'), (TEST_IP6, cc.PORT))
    time.sleep(6)
