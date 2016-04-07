#!/usr/bin/env python

import socket
import sys

import PIL
from PIL import Image

import imgload
import fpgautil

STARTUP_MSG="""
\033[H
\033[2J
        \033[31m__________  _________   \033[39m\033[32m__  ______  ____ \033[39m ________________  __ 
       \033[31m/ ____/ __ \/ ____/   | \033[39m\033[32m/ / / / __ \/ __ \\\033[39m/ ____/_  __/ __ \/ / 
      \033[31m/ /_  / /_/ / / __/ /| |\033[39m\033[32m/ / / / / / / /_/ / \033[39m/     / / / /_/ / /  
     \033[31m/ __/ / ____/ /_/ / ___ \033[39m\033[32m/ /_/ / /_/ / ____/ \033[39m/___  / / / _, _/ /___
    \033[31m/_/   /_/    \____/_/  |_\033[39m\033[32m\____/_____/_/    \033[39m\____/ /_/ /_/ |_/_____/
"""

SERV_ADDR = "127.0.0.1"
SERV_PORT = 2600
MESSAGE = STARTUP_MSG

DEVNAME="/dev/ttyUSB0"

BUF_SIZE = 1024

USAGE = """udpclient: [server|pktgen] addr port\n            client dest port filename""" 
def hexdump(src, length=8):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)


def client(addr, port, filename):
    print "                    sending to:", addr, port

    img = Image.open(filename)

    csock = socket.socket(socket.AF_INET, 
			 socket.SOCK_DGRAM)
    csock.connect((addr, port))  # be a well behaved udp peer 

    #client:
    #   open image file
    #   convert image to fpga format
    #   break fpga into chunks from base address
    #   randomise chunks (CHAOS!!)
    #   sendto chunks
    csock.sendto(MESSAGE, (addr, port))

def server(dev, addr, port):
    print "                    listening on", addr, port
    ssock = socket.socket(socket.AF_INET, 
			 socket.SOCK_DGRAM) 
    ssock.bind((addr, port))

    #server:
    #   create (flat colour) framebuffer
    #   send framebuffer to fpga 
    #   recvfrom packet
    #   extract addr
    #   convert base addr to x,y (annoying, try not to)
    #   work through chunck, updating fb, sending each packet to fpga
    #   show fb

    while True:
	data, addr = ssock.recvfrom(BUF_SIZE) 
	print "received message from:", addr
        print hexdump(data)

def pktgen(addr, port):
    print "                    sending to:", addr, port
    csock = socket.socket(socket.AF_INET, 
			 socket.SOCK_DGRAM)
    csock.connect((addr, port)) 

    while true:
        sock.sendto(MESSAGE, (addr, port))

if __name__ == "__main__":

    if len(sys.argv) <= 2:
        print(USAGE)
        sys.exit()

    mode = sys.argv[1]

    if mode == "client" and len(sys.argv) != 3:
        print USAGE
        exit()

    print(STARTUP_MSG)
    print "                                 ", mode

    if mode == "server":
        server(dev, SERV_ADDR, SERV_PORT)
    elif mode == "client":
        filename = sys.argv[2]
        client(SERV_ADDR, SERV_PORT, filename)
    elif mode == "pktgen":
        pktgen(SERV_ADDR, SERV_PORT)
