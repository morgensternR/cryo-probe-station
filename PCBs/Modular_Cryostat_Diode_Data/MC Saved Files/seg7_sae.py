from machine import Pin, I2C

#i2c = I2C(1, scl=machine.Pin(23), sda=machine.Pin(22))

class CH455G:

    # https://en.wikichip.org/wiki/seven-segment_display/representing_letters
    seven_seg_digits_decode_gfedcba = [
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

    def __init__(self, i2c=None):
        if i2c==None:
            i2c = I2C(1, scl=machine.Pin(23), sda=machine.Pin(22))
        self.i2c = i2c
        self.config(0x11)

    def parse_string(self, msg):
        msg = msg+'    '
        codes = []
        idx = 0
        for m in msg:
            if m == '.':
                if idx>0:
                    idx -= 1
                    codes[idx] |= 0x80
                else:
                    codes.append(0x3F | 0x80)
            elif (ord(m)<ord('0')) | (ord(m)>ord('z')):
                codes.append(0)
            else:
                codes.append(self.seven_seg_digits_decode_gfedcba[ord(m)-ord('0')])
            idx += 1
        return codes[:4]

    def config(self, value):
        i2c = self.i2c
        i2c.writeto(0x24, bytes([value]))

    def display(self, msg = '.1.2.3.4'):
        codes = self.parse_string(msg)
        i2c = self.i2c
        for i in range(4):
            i2c.writeto(52+i, bytes([codes[i]]))


#Example of usage:
'''
d = CH455G()
d.display('55.62')
#d.display('help')
'''
