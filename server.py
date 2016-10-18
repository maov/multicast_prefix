#!/usr/bin/env python
import socket
import sys
import common as cc
import logging
import subprocess


entry_start = '### START AUTOMATIC GENERATED ENTRIES ###\n'
entry_stop = '### END AUTOMATIC GENERATED ENTRIES ###\n'

INTERFACE="eth0"

#read until start tag copy all elements untill end tag, save file and return dict, last entryfile
def open_host_file(host_name=None, ipv6=None):
    lines = []
    with open('/etc/hosts','r') as host_file:
        lines = host_file.readlines()
    if entry_start not in lines :
        ## create start and stop entries
        lines.append(entr_start)
        lines.append(entry_stop)
    start_idx = lines.index(entry_start)
    stop_idx = lines.index(entry_stop)
    new_line = '' if host_name is None else '{0} {1}'.format(ipv6, host_name)
    lines.insert(start_idx + 1, new_line)
    entries = lines[start_idx + 1 : stop_idx]
    key_value = [e.split(' ',1).reverse() for e in entries if ' ' in e]
    with open('/etc/hosts','w') as host_file :
        host_file.write("".join(lines))
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
        common_routes = routes.startswith(cc.COMMON_PREFIX).split(' ')
        prefix_gateway = dict([(e[0],e[3]) for e in common_routes])
        print(routes)
    #what to do when ip/routes change, remove previous entry?!?!?
    if prefix is not None AND prefix not IN prefix_gateway:
        #add route
        route_cmd = 'Adding, ip -6 route add {0} via {1}'.format(prefix, gateway)
        print(route_cmd)
        proc2 = subprocess.Popen(route_cmd, shell=True, stdout=subprocess.PIPE)
        (output,error) = proc2.communicate()
        if error is not None:
            raise exception("something went wrong calling {0} \n{1}".format(cmd, error))
        prefix_gateway[prefix] = gateway
    return prefix_gateway

setup_route()

print(socket.gethostname())

hosts = {}

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('', cc.PORT)
print('starting up on {0}'.format(server_address))

sock.bind((server_address))

open_host_file()



try : 
    while True:
        print(hosts)
        print('waiting for connection')
        data, sender = sock.recvfrom(1500)
        print (str(sender) + '  ' + data.decode('utf-8'))
        data_spl = data.decode('utf-8').split(';')
        #get device that reveived multicast???

        #Check hash hasnt been used yet
        #for lala in hosts where key <> key and prefix  = prefix
        #throw warning if its the case

        #otherwise add the key if it hasnt been addded
        if data_spl[0] not in hosts:
            hosts[data_spl[0]] = { 'ipv6' : data_spl[1], 'prefix' : data_spl[2]} 
            print('New entry added {0} : {1}', data_spl[0], hosts[data_spl[0]]) 
            #update hosts file
            #update route
finally:
    sock.close()
