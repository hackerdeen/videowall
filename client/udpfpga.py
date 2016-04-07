#!/usr/bin/env python

import socket
import sys
from random import shuffle

import PIL
from PIL import Image

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

BUFSIZE = 1024
CHUNKSIZE = 1024

USAGE = """udpclient: [server|pktgen] addr port\n            client dest port filename""" 

SHOW = True
SHUFFLE = False

def client(addr, port, filename):
    print "                    sending to:", addr, port

    hsot = addr,port

    img = Image.open(filename)
    img = img.resize( fpgautil.WALLSIZE, PIL.Image.NEAREST)

    img = fpgautil.thresholdimg(img)
    img = fpgautil.encodeimg(img)

    csock = socket.socket(socket.AF_INET, 
			 socket.SOCK_DGRAM)
    csock.connect(host)  # be a well behaved udp peer 

    #client:
    #   ~~open image file~~
    #   ~~convert image to fpga format~~
    #   break fpga into chunks from base address
    #   ~~randomise chunks (CHAOS!!)~~
    #   sendto chunks

    chunks = fpgautil.chunkimg(img) #list of str's
    if SHUFFLE: shuffle(chunks)

    for msg in chunks:
        csock.sendto(msg, host))

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
	data, addr = ssock.recvfrom(BUFSIZE) 
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

    if len(sys.argv) <= 4:
        print(USAGE)
        sys.exit()

    mode = sys.argv[1]

    print len(sys.argv)
    if mode == "client" and len(sys.argv) != 5:
        print USAGE
        exit()

    print(STARTUP_MSG)
    print "                                 ", mode

    if mode == "server":
        server(SERV_ADDR, SERV_PORT, dev)
    elif mode == "client":
        filename = sys.argv[4]
        client(SERV_ADDR, SERV_PORT, filename)
    elif mode == "pktgen":
        pktgen(SERV_ADDR, SERV_PORT)
