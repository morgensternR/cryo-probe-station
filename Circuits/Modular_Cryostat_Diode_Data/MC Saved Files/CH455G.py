#7 Segment display
import math as m
import time
from machine import Pin, I2C


class CH455G:
    def __init__(self, i2c = None ):
        if i2c == None:
            i2c = I2C(1, scl=machine.Pin(23), sda=machine.Pin(22))
        self.i2c = i2c
        self.scroll = False

    def find_all(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches

    def i2cwrite(self, addr, cmd):
        #self.i2c.try_lock()
        self.i2c.writeto(addr, cmd)
        #self.i2c.unlock()
    def settings(self, cmd):
        if type(cmd) != bytes:
            print("Error command must be in bytes\n")
            print("0[INTENS][7SEG][SLEEP]0[ENA]B\n")
            print("0 000 0 0 0 0")
            return
        self.i2cwrite(0x24, cmd)

    def parse_str(self, data):
        data = data
        #pos = list(self.find_all(data, '.'))
        loc = 0
        output = []
        for i in data:
            #print(i)
            if i == '.':
                if loc > 0:
                    loc -= 1
                    output[loc] |= 0x80
                else:
                    output[loc] = 0x3F|0x80
            elif i == '-':
                output.append(64)
            elif (ord(i)<ord('0')) | (ord(i)>ord('z')):
                output.append(0)
            else:
                output.append(self.seven_seg_digits_decode[ord(i)-ord('0')])
            loc += 1
        return output

    def scroll_text(self, msg):
        while self.scroll:
            for m in range(len(msg)):
                #self.i2c.try_lock()
                self.i2c.writeto(55, bytes([msg[m]]))
                self.i2c.writeto(0x36, bytes([msg[m-1]]))
                self.i2c.writeto(0x35, bytes([msg[m-2]]))
                self.i2c.writeto(0x34, bytes([msg[m-3]]))
                #self.i2c.unlock()
                time.sleep(0.5)
    def display(self, data):
        self.reset()
        message = self.parse_str(data)
        if len(message) > 4:
            self.scroll = True
            self.scroll_text(message)
        else:
            for i in range(4):
                #self.i2c.try_lock()
                self.i2c.writeto(self.count[i], bytes([message[i]]))
                #self.i2c.unlock()

    def reset(self):
        for i in self.count:
            self.i2cwrite(i, self.num[' '])

    #Dictionary and list to use
# https://en.wikichip.org/wiki/seven-segment_display/representing_letters
    seven_seg_digits_decode = [
    #/*  0     1     2     3     4     5     6     7     8     9     :     ;     */
        0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x00, 0x00,
    #/*  <     =     >     ?     @     A     B     C     D     E     F     G     */
        0x00, 0x00, 0x00, 0x00, 0x00, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x3D,
    #/*  H     I     J     K     L     M     N     O     P     Q     R     S     */
        0x76, 0x30, 0x1E, 0x75, 0x38, 0x55, 0x54, 0x5C, 0x73, 0x67, 0x50, 0x6D,
    #/*  T     U     V     W     X     Y     Z     [     \     ]     ^     _     */
        0x78, 0x3E, 0x1C, 0x1D, 0x64, 0x6E, 0x5B, 0x00, 0x00, 0x00, 0x00, 0x00,
    #/*  `     a     b     c     d     e     f     g     h     i     j     k     */
        0x00, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x3D, 0x76, 0x30, 0x1E, 0x75,
    #/*  l     m     n     o     p     q     r     s     t     u     v     w     */
        0x38, 0x55, 0x54, 0x5C, 0x73, 0x67, 0x50, 0x6D, 0x78, 0x3E, 0x1C, 0x1D,
    #/*  x     y     z     */
        0x64, 0x6E, 0x5B ]

    num = {' ':(b'\x00'),
        '0':63,
        '1':6,
        '2':91,
        '3':79,
        '4':102,
        '5':109,
        '6':125,
        '7':7,
        '8':127,
        '9':103,
        'E':121,
        'e':121,
        '-':64}

    count = [0x34,0x35,0x36, 0x37]


#Fix def names
#Get rid of bad code
#change to_bytes
#remove parathesis
d = CH455G()
d.display('12234567890abcdefghijklmnop')