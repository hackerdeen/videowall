import serial
import struct
from time import sleep

def test():
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
    print "sending write command"
    ser.write("\x00\x00\x00\x01\xde\xad\xbe\xef")
    res = ser.read(1)
    print res
    print "sending read command"
    ser.write("\x80\x00\x00\x01")
    res = ser.read(4)
    print res, len(res), [ord(x) for x in res]
    print "%x"%struct.unpack("<I", res)[0]


def all_colour(ser, colour):
    # only setting screen 0 ATM
    colour = colour << 29
    for addr in xrange(200*150):
        addr_string = struct.pack(">I", addr)
        for char in addr_string:
            ser.write(char)
        colour_string = struct.pack(">I", colour)
        for char in colour_string:
            ser.write(char)
        ack = ser.read(1)
        if ack <> "A":
            print ack
        print "set %x to %08x"%(addr, colour)
    print "set all to %08x"%colour 

def cycle_colour(ser):
    for i in xrange(8):
        all_colour(ser, i)
        sleep(4)

def write_colour(ser, x, y, c):
    addr = x+y*200
    write_colour(ser, addr, c)

#takes a int containing the address and a 4 tuple with colour
def write_colour(ser, addr, c):
    data = struct.pack(">I>I",addr,c)
    for c in data:
        ser.write(c)
    ack = ser.read(1)
    #print "set %x (%d, %d) to %x (%x)"%(addr, x, y, c, colour)
    if ack <> "A":
        print ack

def square_colours(x, y):
    if ((x/10) % 2) == 0 and ((y/10) % 2) == 0:
        return 7
    else:
        return 0

def half_colour(ser, colour):
    for x in xrange(100, 200):
        for y in xrange(150):
            write_colour(ser, x, y, colour)
        
def squares(ser):
    for x in xrange(800):
        for y in xrange(600):
            write_colour(ser, x, y, square_colours(x, y))
            
if __name__=="__main__":
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
    #cycle_colour(ser)
    #squares(ser)
    all_colour(ser, 5)
    print "On to half colour"
    half_colour(ser, 0)
