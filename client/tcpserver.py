#!/usr/bin/env python

import sys
import socket
import PIL
from PIL import Image
import StringIO

import fpgautil

STARTUP_MSG="""
\033[H
\033[2J
        \033[31m__________  _________  \033[39m\033[32m________________\033[39m  ________________  __ 
       \033[31m/ ____/ __ \/ ____/   |\033[39m\033[32m/_  __/ ____/ __ \\\033[39m/ ____/_  __/ __ \/ /
      \033[31m/ /_  / /_/ / / __/ /| |\033[39m\033[32m / / / /   / /_/ /\033[39m /     / / / /_/ / /  
     \033[31m/ __/ / ____/ /_/ / ___ |\033[39m\033[32m/ / / /___/ ____/\033[39m /___  / / / _, _/ /___
    \033[31m/_/   /_/    \____/_/  |_\033[39m\033[32m/_/  \____/_/    \033[39m\____/ /_/ /_/ |_/_____/
"""                                                                        

SERV_ADDR = '127.0.0.1'
SERV_PORT = 2600
BUFSIZE = 4096

SHOW = False
DEVNAME = "/dev/ttyUSB0"

# tcp listener, accepts raw images over a socket
# you can send an image with nc like so:
#   $ nc -N 127.0.0.1 2600 < morninglake.png
if __name__ == "__main__":

    print STARTUP_MSG
    print "                     listening on", SERV_ADDR, SERV_PORT
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERV_ADDR, SERV_PORT))
    s.listen(1) #only allow one connection to queue at a time

    imgdata = ""

    while True:
        conn, addr = s.accept() 
        sys.stdout.write("*")
        sys.stdout.flush()

        while True:
            data = conn.recv(BUFSIZE)
            if not data: break
            imgdata += data
            sys.stdout.write(".")
            sys.stdout.flush()
        conn.close()

        imgbuf = StringIO.StringIO() 
        imgbuf.write(imgdata) 
        imgbuf.seek(0)

        img = Image.open(imgbuf)
        if SHOW: img.show()

        img = img.resize(fpgautil.WALLSIZE, PIL.Image.NEAREST) 


        fpgaimg = fpgautil.encodeimg(img)
        if SHOW: fpgaimg.show()

        fpgadata = list(img.getdata())
        fpgautil.sendtofpga(DEVNAME, fpgadata)
        print "next image plz..."
