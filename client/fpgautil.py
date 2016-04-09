#!/usr/bin/env python

import PIL
from PIL import Image
import struct
import sys
from random import shuffle

import fpgaserial

SCREENSWIDE = 3
SCREENSTALL = 3
SCREENSIZE = 800, 600
WALLSIZE = SCREENSIZE[0]*SCREENSWIDE,SCREENSIZE[1]*SCREENSTALL
CHUNKSIZE = 1004

LIMIT = 64
SHOW = False
SHOW = True

def hexdump(src, length=8):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)

# extract a pixel from the image across the 9 regions and encode it into 4 bytes
def packpixel(img, srcx, srcy, dstw, dsth):
    pixels = []
    
    widths = [0, dstw, dstw*2]
    heights = [0, dsth, dsth*2]

    for x in widths:
        for y in heights:
            pixels.append(img.getpixel((srcx+x,srcy+y)))

    pixel = 0x00000000

    for p in pixels:
        r = 1 if p[0] > LIMIT else 0
        g = 1 if p[1] > LIMIT else 0
        b = 1 if p[2] > LIMIT else 0

        pixel |= ((0x01 & r) << 2)
        pixel |= ((0x01 & g) << 1)
        pixel |= (0x01 & b)

        pixel = pixel << 3

    pixel = pixel << 2 #shift up to be more wrong

    fields = struct.unpack('4B', struct.pack('>I', pixel))
    return fields

# take an rgba pixel and encode it into the spread 9 display pixels
def unpackpixel(img, srcx, srcy, dstw, dsth, pixel):
    widths = [0, dstw, dstw*2]
    heights = [0, dsth, dsth*2]

    positions = []

    for x in widths:
        for y in heights:
            positions.append((x,y))

    data = ''.join([chr(x) for x in pixel])
    pixel = struct.unpack(">I", data)

    pixel = pixel[0] >> 5 #shift down to be less wrong
    pixels = []

    for p in range(9):
        r = (0x04 & pixel)
        g = (0x02 & pixel)
        b = (0x01 & pixel)

        r = 255 if r else 0
        g = 255 if g else 0
        b = 255 if b else 0

        pixels.append( (positions.pop(), (r, g, b)))
        pixel = pixel >> 3

    for p in pixels:
        x = p[0][0]
        y = p[0][1]
        col = p[1]
        img.putpixel((srcx+x,srcy+y), col)

def thresholdimg(img):
    old = list(img.getdata())
    new = []

    for x in old:
        r = 255 if x[0] > LIMIT else 0
        g = 255 if x[1] > LIMIT else 0
        b = 255 if x[2] > LIMIT else 0
        new.append((r,g,b))

    newimg = Image.new("RGB", WALLSIZE)
    newimg.putdata(new)

    return newimg

def encodeimg(img):
    fpgaimg = Image.new("RGBA",SCREENSIZE, color=(255,255,255,255))

    for x in range(SCREENSIZE[0]):
        for y in range(SCREENSIZE[1]):
            pixel = packpixel(img,x, y, SCREENSIZE[0], SCREENSIZE[1])
            fpgaimg.putpixel((x, y), pixel)
    return fpgaimg

def decodeimg(img):
    newimg = Image.new("RGB", WALLSIZE, color=(0,0,0)) 

    pixels = []
    for x in range(SCREENSIZE[0]):
        for y in range(SCREENSIZE[1]):
            p = img.getpixel((x,y)) 
            pixels.append(unpackpixel(newimg,x, y, SCREENSIZE[0], SCREENSIZE[1], p))
    return newimg

#lets take in an array of pixels, likke pil.getdata gives
def sendtoimgfpga(devname, img):
    addr = 0
    pixeldata = img.getdata()
    for p in pixeldata:
        fpgaserial.write_colour(devname, addr, p)
        addr = addr+1

def sendtochunkfpga(devname, chunks):
    print "lol"
    for chunk in chunks:
        addr = struct.unpack("I", chunk[0:4]) 
        addr = addr[0]
        pixels = strtopix(chunk[4:]) 

        for p in pixels:
            p = ord(p[0]),ord(p[1]),ord(p[2]),ord(p[3])
                
            fpgaserial.write_colour(devname, addr, p)
            addr = addr+1

def chunkimg(img, size):
    chunks = []
    datasz = size-4
    pixcount = datasz/4

    imgsize = img.size[0] * img.size[1]

    if not(imgsize % size):
        print "BAD DATA YOU FUCK WIT"

    pixels = list(img.getdata())

    for addr in range(imgsize/pixcount):
        baddr = addr*pixcount
        off = baddr+pixcount

        subarr = pixels[baddr:off]
        data = pixtostr(subarr)

        chunk = struct.pack("I",baddr)
        chunk += data
        chunks.append(chunk)
    return chunks

def chunktoimg(img, chunks):
    for chunk in chunks:
        addr = struct.unpack("I", chunk[0:4]) 
        addr = addr[0]

        pixels = strtopix(chunk[4:]) 

        for p in pixels:
            pos = (addr%SCREENSIZE[0], addr/SCREENSIZE[0])
            p = ord(p[0]),ord(p[1]),ord(p[2]),ord(p[3])

            img.putpixel(pos , p)
            addr = addr+1

def pixtostr(pix):
    s = ""
    for p in pix:
        s += chr(p[0])
        s += chr(p[1])
        s += chr(p[2])
        s += chr(p[3])
    return s

def strtopix(s):
    n = 4
    l = list(s)
    return [l[i:i + n] for i in range(0, len(l), n)]

if __name__ == "__main__":
   
    if len(sys.argv) == 2:
        if sys.argv[1] == "show":
            SHOW = True

    srcimg = Image.open("morninglake.png")
    srcimg = srcimg.resize(WALLSIZE, PIL.Image.NEAREST) 
    if SHOW: srcimg.show()

    newimg = thresholdimg(srcimg)
    if SHOW: newimg.show()

    fpgaimg = encodeimg(newimg)
    if SHOW: fpgaimg.show()

    chunks = chunkimg(fpgaimg, CHUNKSIZE)
    shuffle(chunks)
    chunkimg = Image.new("RGBA", SCREENSIZE, (0,0,0,255))

    chunktoimg(chunkimg, chunks)
    if SHOW: chunkimg.show()

    chunkimg = decodeimg(chunkimg)
    if SHOW: chunkimg.show()

    newimg = decodeimg(fpgaimg)
    if SHOW: newimg.show()
