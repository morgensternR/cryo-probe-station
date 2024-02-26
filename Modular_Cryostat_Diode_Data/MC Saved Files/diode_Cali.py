import time
import mcp3421 as mcp
import adc_cali_board as adc_cali
from machine import Pin, I2C, SoftI2C
from sys import stdin, stdout

i2cc = SoftI2C(scl=Pin(29, Pin.PULL_UP), sda=Pin(28, Pin.PULL_UP))
dev = mcp.MCP3421(i2cc)

#Driver Object
i2c0 = I2C(1, scl=Pin(23, Pin.PULL_UP), sda=Pin(22, Pin.PULL_UP))
switch = Pin(27, Pin.OUT)
sw_calibrator = adc_cali.adc_cali(i2c = i2c0)
sw_calibrator.switch_0()
#sw_calibrator.on_100k()
switch.value(0)

while True:
    line = stdin.readline()
    if line == "switch 0\n":
        switch.value(0)
    elif line == 'reset\n':
        supervisor.reload()
    elif line == "switch\n":
        if switch.value() == 1:
            switch.value(0)
        else: switch.value(1)
    elif line =="spam_read\n":
        dev.read_adc()
    elif line == "read\n":
        print(dev.read_adc())
    elif line == "100K\n":
        sw_calibrator.current_off()
        sw_calibrator.on_100k()
    elif line == "120K\n":
        sw_calibrator.current_off()
        sw_calibrator.on_120k()
    elif line == "140K\n":
        sw_calibrator.current_off()
        sw_calibrator.on_140k()
    elif line == "160K\n":
        sw_calibrator.current_off()
        sw_calibrator.on_160k()
    elif line == "180K\n":
        sw_calibrator.current_off()
        sw_calibrator.on_180k()
        
        
    

    
    
    