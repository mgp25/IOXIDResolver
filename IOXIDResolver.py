#!/usr/bin/python

import sys, getopt

from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_NONE
from impacket.dcerpc.v5.dcomrt import IObjectExporter

def show_help():
    print('IOXIDResolver.py -t <target>')
    sys.exit()

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"ht:",["target="])
        if opts == []:
            show_help()
    except getopt.GetoptError:
        print('IOXIDResolver.py -t <target>')

    target_ip = "192.168.1.1"

    for opt, arg in opts:
        if opt == '-h':
            show_help()
        elif opt in ("-t", "--target"):
            target_ip = arg

    authLevel = RPC_C_AUTHN_LEVEL_NONE

    stringBinding = r'ncacn_ip_tcp:%s' % target_ip
    rpctransport = transport.DCERPCTransportFactory(stringBinding)

    portmap = rpctransport.get_dce_rpc()
    portmap.set_auth_level(authLevel)
    portmap.connect()

    objExporter = IObjectExporter(portmap)
    bindings = objExporter.ServerAlive2()

    print("[*] Retrieving network interface of " + target_ip)

    #NetworkAddr = bindings[0]['aNetworkAddr']
    for binding in bindings:
        NetworkAddr = binding['aNetworkAddr']
        print("Address: " + NetworkAddr)

if __name__ == "__main__":
   main(sys.argv[1:])
