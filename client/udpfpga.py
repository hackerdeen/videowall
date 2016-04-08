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

USAGE = """udpclient: pktgen addr port\n           server addr port devname\n           client dest port filename""" 

SHOW = True
SHUFFLE = False

def client(addr, port, filename):
    print "                    sending to:", addr, port

    host = addr,port

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
    #   ~~break fpga into chunks from base address~~
    #   ~~randomise chunks (CHAOS!!)~~
    #   ~~sendto chunks~~
    # done?

    chunks = fpgautil.chunkimg(img) #list of str's
    if SHUFFLE: shuffle(chunks)

    for msg in chunks:
        csock.sendto(msg, host)

def server(addr, port, dev):
    host = addr,port

    ssock = socket.socket(socket.AF_INET, 
			 socket.SOCK_DGRAM) 
    ssock.bind(host)

    print "                  setting up fb, encoding, show:", SHOW
    fb = Image.new("RGBA", fpgautil.SCREENSIZE, (0, 255, 0, 255))
    displayimg = fpgautil.decodeimg(fb)

    if SHOW: fb.show()
    if SHOW: displayimg.show()

    fgpautil.sendtofpga(dev, fb)

    #server:
    #   ~~create (flat colour) framebuffer~~
    #   ~~create a buffer to display~~
    #   ~~send framebuffer to fpga ~~
    #   ~~recvfrom packet~~
    #   ~~work through chunck, updating fb, sending each packet to fpga~~
    #   ~~show fb~~

    print "           listening on", host[0], host[1], "controlling", dev
    while True:
	data, peer = ssock.recvfrom(BUFSIZE) 
	print "received message from:", peer 
        print hexdump(data)
        fpgautil.chunktoimg(fb, [data])
        if SHOW: fb.show()

def pktgen(addr, port):
    unktoimg(chunkimg, chunks)
    if SHOW: chunkimg.show()
    print "                    sending to:", addr, port
    csock = socket.socket(socket.AF_INET, 
			 socket.SOCK_DGRAM)
    csock.connect((addr, port)) 

    while true:
        sock.sendto(MESSAGE, (addr, port))

if __name__ == "__main__":

    print sys.argv, len(sys.argv)
    if len(sys.argv) < 4:
        print(USAGE)
        sys.exit()

    mode = sys.argv[1]
    #SERV_ADDR = sys.argv[2]
    #SERV_PORT = str(sys.argv[3])
    #DEVNAME
    #filename

    if mode == "server" and len(sys.argv) != 5:
        print USAGE
        exit()
    if mode == "client" and len(sys.argv) != 5:
        print USAGE
        exit()

    print(STARTUP_MSG)
    print "                                 ", mode

    if mode == "server":
        DEVNAME = sys.argv[4]
        server(SERV_ADDR, SERV_PORT, DEVNAME)
    elif mode == "client":
        filename = sys.argv[4]
        client(SERV_ADDR, SERV_PORT, filename)
    elif mode == "pktgen":
        pktgen(SERV_ADDR, SERV_PORT)
