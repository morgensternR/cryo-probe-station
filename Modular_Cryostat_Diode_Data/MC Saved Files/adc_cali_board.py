import AW9523B as leddrv

class adc_cali:
    def __init__(self, i2c, I2C_address = 0x5b):
        self.adc_cali = leddrv.AW9523B(I2C_address, i2c)
        self.adc_cali.reset()
        self.adc_cali.led_mode(True)
        self.current_step = 104 # Imax * (x/255) current stepping...Imax = 37mA
        
    def on_100k(self):
        self.adc_cali.current_dim('P0_4', self.current_step) #15mA
        self.adc_cali.current_dim('P0_5', self.current_step)
    def on_120k(self):
        self.adc_cali.current_dim('P0_6', self.current_step) #15mA
        self.adc_cali.current_dim('P0_7', self.current_step)
    def on_140k(self):
        self.adc_cali.current_dim('P1_0', self.current_step) #15mA
        self.adc_cali.current_dim('P1_1', self.current_step)
    def on_160k(self):
        self.adc_cali.current_dim('P1_2', self.current_step) #15mA
        self.adc_cali.current_dim('P1_3', self.current_step)
    def on_180k(self):
        self.adc_cali.current_dim('P1_4', self.current_step) #15mA
        self.adc_cali.current_dim('P1_5', self.current_step)
    def on_200k(self):
        self.adc_cali.current_dim('P1_6', self.current_step) #15mA
        self.adc_cali.current_dim('P1_7', self.current_step)
        
    def current_off(self):
        self.adc_cali.current_dim('P0_4', 0) #15mA
        self.adc_cali.current_dim('P0_5', 0)
        self.adc_cali.current_dim('P0_6', 0) #15mA
        self.adc_cali.current_dim('P0_7', 0)
        self.adc_cali.current_dim('P1_0', 0) #15mA
        self.adc_cali.current_dim('P1_1', 0)
        self.adc_cali.current_dim('P1_2', 0) #15mA
        self.adc_cali.current_dim('P1_3', 0)
        self.adc_cali.current_dim('P1_4', 0) #15mA
        self.adc_cali.current_dim('P1_5', 0)
        self.adc_cali.current_dim('P1_6', 0) #15mA
        self.adc_cali.current_dim('P1_7', 0)
        
    def reset(self):
        self.adc_cali.reset()
        
    def led_mode(self, on = False):
        self.adc_cali.led_mode(on)
        
    def switch_0(self):
        self.adc_cali.current_dim('P0_0', self.current_step)
        self.adc_cali.current_dim('P0_1', self.current_step)
    def switch_1(self):
        self.adc_cali.current_dim('P0_2', self.current_step)
        self.adc_cali.current_dim('P0_3', self.current_step)
        
    def switch_off(self):
        self.adc_cali.current_dim('P0_0', 0)
        self.adc_cali.current_dim('P0_1', 0)
        self.adc_cali.current_dim('P0_2', 0)
        self.adc_cali.current_dim('P0_3', 0)