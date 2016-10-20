#!/usr/bin/env python
import socket
import sys
import common as cc
import time
import logging
import hashlib
import argparse


LOCAL_IP6="{0}::1".format(cc.COMMON_PREFIX)
TEST_IP6="{0}::3".format(cc.COMMON_PREFIX)
PREFIX= "{0}:{1}:{2}::/80"

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
hostname = socket.gethostname()
sock.close()

def local_prefix() :
    #use hashlib to generate prefix, and hope for no clash
    prefix_seed = hashlib.md5(hostname.encode("utf-8")).hexdigest()[0:8]
    return PREFIX.format(cc.COMMON_PREFIX,prefix_seed[0:4], prefix_seed[4:8])

def run_client(interval) :
    while True:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        msg = '{0};{1};{2}'.format(hostname,LOCAL_IP6, local_prefix())
        print('Sending multicast {0}'.format(msg.encode('utf-8')))
        sock.sendto(msg.encode('utf-8'), (TEST_IP6, cc.PORT))
        time.sleep(interval)

parser = argparse.ArgumentParser()
parser.add_argument('gen_prefix', help='generates ipv6/80 prefix using md5 on hostname') 
parser.add_argument('interval', help='Interval in seconds between each multicast request',type=int, default=30)
args = parser.parse_args()

if args.gen_prefix :
    print(local_prefix())
else :
    run_client(10)
