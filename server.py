#!/usr/bin/env python3
import socket
import sys
import common as cc
import logging
import subprocess
import struct


entry_start = '### START AUTOMATIC GENERATED ENTRIES ###\n'
entry_stop = '### END AUTOMATIC GENERATED ENTRIES ###\n'

INTERFACE="eth0"

#read until start tag copy all elements untill end tag, save file and return dict, last entryfile
def open_host_file(host_name=None, ipv6=None, file_path='/etc/hosts'):
    lines = []
    with open(file_path, 'r') as host_file:
        lines = host_file.readlines()
    if entry_start not in lines :
        ## create start and stop entries
        lines.append(entry_start)
        lines.append(entry_stop)
    start_idx = lines.index(entry_start)
    stop_idx = lines.index(entry_stop)
    if host_name is not None :
        lines.insert(start_idx + 1, '{0} {1}\n'.format(ipv6, host_name))
        stop_idx = stop_idx + 1
    with open(file_path,'w') as host_file :
        host_file.write("".join(lines))
    entries = lines[start_idx + 1 : stop_idx]
    key_value = [e.strip('\n').split(' ',1)[::-1] for e in entries if ' ' in e]
    return dict(key_value)


def setup_route(prefix=None, gateway=None):
    #Get routes
    cmd = 'ip -6 route'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (output, err) = proc.communicate()
    prefix_gateway = {}
    if err is not None:
        raise exception("something went wrong calling {0} \n{1}".format(cmd, err))
    else: 
        routes = output.decode('utf-8').split("\n")
        common_routes = [ e.split(' ') for e in routes if e .startswith(cc.COMMON_PREFIX)]
        prefix_gateway = dict([(e[0],e[3]) for e in common_routes])
        print(routes)
    #what to do when ip/routes change, remove previous entry?!?!?
    if prefix is not None and prefix not in prefix_gateway:
        #add route
        route_cmd = 'ip -6 route add {0} via {1}'.format(prefix, gateway)
        print(route_cmd)
        proc2 = subprocess.Popen(route_cmd, shell=True, stdout=subprocess.PIPE)
        (output,error) = proc2.communicate()
        if error is not None:
            raise exception("something went wrong calling {0} \n{1}".format(cmd, error))
        prefix_gateway[prefix] = gateway
    return prefix_gateway

hosts = open_host_file(file_path='testfile.txt') 
print(hosts)

try : 
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #group = socket.inet_pton(socket.AF_INET6, cc.GROUP_6)
    server_address = (cc.GROUP_6, cc.PORT)
    print('starting up on {0} listening to multicast {1}'.format(server_address, cc.GROUP_6))
     
    sock.bind(server_address)

    group = socket.inet_pton(socket.AF_INET6, cc.GROUP_6) + struct.pack('=I', socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, group)

    print('waiting for connection')
    while True:
        data, sender = sock.recvfrom(1500)
        print('got connection {0}'.format(sender))
        #print (str(sender) + '  ' + data.decode('utf-8'))
        data_spl = data.decode('utf-8').split(';')
        hostname = data_spl[0]
        #add the key if it hasnt been addded
        if hostname not in hosts:
            host_entry = { 'ipv6' : data_spl[1], 'prefix' : data_spl[2]}
            #update hosts file
            print(hostname)
            print(host_entry)
            hosts = open_host_file(host_name=hostname, ipv6=host_entry['ipv6'], file_path='testfile.txt')
            #update route
            setup_route(host_entry['prefix'], host_entry['ipv6'])
            hosts[hostname] = host_entry
            print('New entry added {0} : {1}', hostname, hosts[hostname]) 
finally:
    sock.close()
