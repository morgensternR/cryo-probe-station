#Diode Query Readout
import mcp3421 as mcp
import seg7_sae as seg7
from machine import Pin, I2C, SoftI2C
from sys import stdin, stdout
import gc
import ujson
import select


i2c1 = I2C(1, scl=Pin(23, Pin.PULL_UP), sda=Pin(22, Pin.PULL_UP))
i2c0 = SoftI2C(scl=Pin(29, Pin.PULL_UP), sda=Pin(28, Pin.PULL_UP))
diode_40k = mcp.MCP3421(i2c1, slope = 15971, offset =24 ) #Decimal address:  104  | Hexa address:  0x68
#slope = 15971.195616075353 offset = 24.4957468050373
led_40k = seg7.CH455G(i2c1)


diode_4k = mcp.MCP3421(i2c0, slope = 15964, offset = 19 ) #Decimal address:  104  | Hexa address:  0x68
#slope = 15964.727046904583 offset = 18.546311696248097
led_4k = seg7.CH455G(i2c0)





def readUSB():
    global ONCE, CONTINUOUS, last
    gc.collect()
    while stdin in select.select([stdin], [], [], 0)[0]:
        #print('Got USB serial message')
        gc.collect()
        cmd = stdin.readline()
        #print(type(cmd), repr(cmd))
        cmd = cmd.strip().upper()
        if len(cmd)>0:
            do_command(cmd)

def writeUSB(msg):
    print(ujson.dumps(msg))
    
def do_command(cmd):
    global diode_40k, diode_4k
    # print('cmd', cmd)
    cmd = cmd.split()
    #print('cmd', cmd)
    if len(cmd)>1:
        params = cmd[1:]
    else:
        params = []
    cmd = cmd[0]
    print(cmd, params)
    if len(cmd):  # respond to command
        if (cmd =='READ'):
            writeUSB({'40K' : diode_40k.read_adc_v(), '4K' : diode_4k.read_adc_v()})
        elif (cmd == 'SHOW'):
            led_40k.display(str(params[0]))
            led_4k.display(str(params[1]))
        else:
            writeUSB('Not understood')

while True:
    readUSB()
