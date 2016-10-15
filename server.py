#!/usr/bin/env python
import socket
import sys
import common as cc
import logging

entry_start = '### START AUTOMATIC GENERATED ENTRIES ###\n'
entry_stop = '### END AUTOMATIC GENERATED ENTRIES ###\n'

#read until start tag copy all elements untill end tag, and return dict, last entryfile
#if no start_tag create start and end tag
def open_host_file():
    lines = []
    with open('/etc/hosts','r') as host_file:
        lines = host_file.readlines()
    if entry_start not in lines :
        ## create start and stop entries
        with open('/etc/hosts','a') as host_file:
            host_file.write(entry_start)
            host_file.write('\n')
            host_file.write(entry_stop)
            return {}
    else :
        ## Make list of lines with entries
        ## return list
        print('lalal')
        start_idx = lines.index(entry_start)
        stop_idx = lines.index(entrystop)
        entries = lines[start_idx + 1 : stop_idx]
        key_value = [e.split(' ',1).reverse() for e in entries if ' ' in e]
        return dict(key_value)

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
