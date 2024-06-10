import time
import mcp3421 as mcp
import adc_cali_board as adc_cali
import seg7_sae as seg7
from machine import Pin, I2C, SoftI2C
from sys import stdin, stdout

i2c0 = I2C(1, scl=Pin(23, Pin.PULL_UP), sda=Pin(22, Pin.PULL_UP))
#i2cc = SoftI2C(scl=Pin(29, Pin.PULL_UP), sda=Pin(28, Pin.PULL_UP))


diode = mcp.MCP3421(i2c0, slope = 15971, offset =10 ) #Decimal address:  104  | Hexa address:  0x68
led = seg7.CH455G(i2c0)
sw_calibrator = adc_cali.adc_cali(i2c = i2c0) #Decimal address:  104  | Hexa address:  0x68
sw_calibrator.current_off()
res_list = [sw_calibrator.on_100k,
            sw_calibrator.on_120k,
            sw_calibrator.on_140k,
            sw_calibrator.on_160k,
            sw_calibrator.on_180k]

def demo_test():
    while True:
        for i in res_list:
            
            i()
            for i in range(120):
                data = diode.read_adc_v()
                #time.sleep(0.1)
                print(data)
                led.display(str(data))
            print(str(data))
            time.sleep(0.5)
            sw_calibrator.current_off()

demo_test()       
