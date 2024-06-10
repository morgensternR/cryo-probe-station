from machine import Pin, I2C
import mcp3421 as mcp

class TCA9548A:
    def __init__(self, i2c, addr=112):
        self.i2c = i2c
        self.addr = addr

    def read_reg(self):
        data = bytearray(1)
        self.i2c.readfrom_into(self.addr, data)
        return data
    
    def write_reg(self, adc_int, enable = True):
        #Assume to reset to default disable state before reading. Dont require more than 1 to be enabled
        self.i2c.writeto(self.addr, bytes([0x00]))
        
        data = (2**adc_int)*int(enable) #0 to disbale, 1 to enable
        self.i2c.writeto(self.addr, bytes([data]))

i2c = I2C(1, scl=machine.Pin(23), sda=machine.Pin(22))
i2c_mux = TCA9548A(i2c)
diode_list = [0,0,0,0,0,0,0,0]

for i in range(1):
    i2c_mux.write_reg(i)
    diode_list[i] = mcp.MCP3421(i2c)
    diode_list[i].set_config()
def read(i):
    i2c_mux.write_reg(i)
    return(diode_list[i].read_adc())
    
#i2c_mux.write_reg(0)
#dev0 = mcp.MCP3421(i2c)
#dev0.set_config()

#dev = mcp.MCP3421(i2c)
#To start the mcp objects, I require opening the i2c since the mcp
