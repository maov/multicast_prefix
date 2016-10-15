#!/usr/bin/env python
import socket
import sys
import common as cc
import time
import logging

while True:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    msg = '{0};{1};{2}'.format(socket.gethostname(),'fdee:f345:543f:0:a00::1/64', 'fdee:f345:543f:0:a00::/80')
    print('Sending multicast {0}'.format(msg.encode('utf-8')))
    sock.sendto(msg.encode('utf-8'), ('', cc.PORT))
    time.sleep(6)
