#!/usr/bin/env python3
import socket
import sys
import common as cc
import time
import logging
import hashlib
import argparse


TEST_IP6="{0}::3".format(cc.COMMON_PREFIX)
DOCKER_IPV6_RANGE= "{0}:{1}::/80"
HOST_IPV6="{0}::{1}"

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
hostname = socket.gethostname()
host_enc = hostname.encode("utf-8")
sock.close()

def local_prefix(seed, formatable_str, parts=2) :
    #use hashlib to generate prefix, and hope for no clash
    prefix_length=parts*4
    prefix_seed = hashlib.md5(seed).hexdigest()[0:prefix_length]
    prefix = ":".join([prefix_seed[e*4 - 4 : e*4] for e in range(1,parts + 1)])
    return formatable_str.format(cc.COMMON_PREFIX,prefix)

def run_client(interval) :
    while True:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        msg = '{0};{1};{2}'.format(hostname,local_prefix(host_enc, HOST_IPV6), local_prefix(host_enc, DOCKER_IPV6_RANGE))
        print('Sending multicast {0}'.format(msg.encode('utf-8')))
        sock.sendto(msg.encode('utf-8'), (cc.GROUP_6, cc.PORT))
        time.sleep(interval)

parser = argparse.ArgumentParser()
parser.add_argument('--prefix_hostname', help='generates ipv6/80 prefix using md5 on hostname', action="store_true") 
parser.add_argument('--interval', help='Interval in seconds inbetween each multicast request',type=int, default=30)
parser.add_argument('--gen_host_ipv6', help='generate prefix from input using md5', type=str, default=None)
args = parser.parse_args()


if args.prefix_hostname :
    print(local_prefix(host_enc, DOCKER_IPV6_RANGE))
elif args.gen_host_ipv6:
    gen_name = args.gen_host_ipv6.encode("utf-8")
    print(local_prefix(gen_name, HOST_IPV6))    
else :
    run_client(args.interval)
