# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:01:15 2023

@author: rdm8
"""

import scipy.interpolate
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

#import Data
data = pd.read_csv(r'C:\Users\rdm8\Downloads\diode_data.csv')
#df.to_pickle('/Drive Path/df.pkl')    #to save the dataframe, df to 123.pkl

data_X_down = data['Temperature'][:26798].reset_index()
data_X_up = data['Temperature'][26797:]

data_dt670_a_down = data['dt670_A'][:26798] 
data_dt670_a_up = data['dt670_A'][26798:] 

data_dt670_b_down = data['dt670_B'][:26798] 
data_dt670_b_up = data['dt670_B'][26798:] 

# data_X_up.to_pickle(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\data_X_up.pkl')
# data_dt670_a_up.to_pickle(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\data_dt670_a_up.pkl')
# data_dt670_b_up.to_pickle(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\data_dt670_b_up.pkl')

# data_X_up.to_json(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\data_X_up')
# data_dt670_a_up.to_json(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\data_dt670_a_up')
# data_dt670_b_up.to_json(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\data_dt670_b_up')

# plot lines 
# plt.plot(data_X_down, data_dt670_a_down, label = "DT670_A Down") 
# plt.plot(data_X_up, data_dt670_a_up, label = "DT670_A up") 
# plt.plot(data_X_down, data_dt670_b_down, label = "DT670_B Down") 
# plt.plot(data_X_up, data_dt670_b_up, label = "DT670_B up") 
plt.plot( data_dt670_a_down,(data_X_up[:26798]['Temperature']-data_X_down), label = "DT670_A Down") 
plt.plot( data_dt670_a_up,data_X_up['Temperature'], label = "DT670_A up") 

# dt670_b_interp = scipy.interpolate.interp1d(data_X_up , data_dt670_b_up)

# plt.plot(data_X_up, dt670_b_interp(data_X_up), label = "DT670_B FIT Scipy") 


# yinterp = np.interp(data_X_up, data_X_up, data_dt670_b_up)

# plt.plot(data_X_up, yinterp, label = 'NP Fit')
#plt.plot(data['dt670_A'][:26798], (data_X_up[:26798]-data_X_down)['Temperature'])

plt.ylabel('Temp (K)')
plt.xlabel('Voltage (V)')
plt.legend() 

plt.show()

#find y-value associated with x-value of 13
data.reindex(index=data.index[::-1])

#%%
import pandas as pd

import numpy as np
import time
import serial
import scipy.interpolate
import pyvisa
import ujson 
from datetime import date

#port.close()
rm = pyvisa.ResourceManager()
print(rm.list_resources())
port = serial.Serial('COM9', timeout=1)

data = pd.read_csv(r'C:\Users\rdm8\Downloads\diode_data.csv')

data_X_down = data['Temperature'][:26798]
data_X_up = data['Temperature'][26798:]

data_dt670_a_down = data['dt670_A'][:26798] 
data_dt670_a_up = data['dt670_A'][26798:] 

data_dt670_b_down = data['dt670_B'][:26798] 
data_dt670_b_up = data['dt670_B'][26798:] 


dt670_a_40k_interp = scipy.interpolate.interp1d(data_dt670_a_up, data_X_up )
dt670_b_4k_interp = scipy.interpolate.interp1d(data_dt670_b_up, data_X_up)

filedir = r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\diode_data_new1'+str(date.today())+'.csv'
#try:
start_time = time.time()
while True:
    try:
        
        port.write(b'read\r\n')
        data_grab = ujson.loads(port.readlines()[1].decode("utf-8"))
         
        temp_40k = dt670_a_40k_interp(data_grab['40K'])
        temp_4k = dt670_b_4k_interp(data_grab['4K'])
         
        show_string = f'show {round(float(temp_40k), 3)} {round(float(temp_4k), 3)}\r\n'
        print(show_string)
        port.write(bytes(show_string, 'utf-8'))
        port.readlines()#Read  Junk Echo from serial
        data = {
        'Time': [time.time() - start_time],
        '40K Temp': temp_40k,
        '40K Voltage': data_grab['40K'],
        '4K': temp_4k,
        '4K Voltage':  data_grab['4K']
        }
        print(data)
        # convert array into dataframe
        DF = pd.DataFrame(data)
          
         # save the dataframe as a csv file
        DF.to_csv(filedir, mode='a', index=False, header=False)
         
        time.sleep(0.2)
            
    except ValueError:
        print('Value Error')
        show_string = 'show err err\r\n'
        port.write(bytes(show_string, 'utf-8'))
        port.readlines()#Read  Junk Echo from serial
        pass
        
#%%
import ujson
import pandas as pd
import scipy.interpolate
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

#Made calibrated lists from scipy interpolation due to size constraints
data = pd.read_csv(r'C:\Users\rdm8\Downloads\diode_data.csv')

cut_off = 26796
data_X_up = data['Temperature'][cut_off:]

data_dt670_a_up = data['dt670_A'][cut_off:] 

data_dt670_b_up = data['dt670_B'][cut_off:] 


dt670_a_40k_interp = scipy.interpolate.interp1d(data_X_up, data_dt670_a_up )
dt670_b_4k_interp = scipy.interpolate.interp1d(data_X_up, data_dt670_b_up)




new_x_list = np.linspace(300,2, 300*6).round(4)

# output 
with open(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\x_list.json', 'w') as f:
    ujson.dump(new_x_list.tolist(), f)
    
# Closing file
f.close()

new_dt670_a = dt670_a_40k_interp(new_x_list).round(4)

# output 
with open(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\dt670_a.json', 'w') as f:
    ujson.dump(new_dt670_a.tolist(), f)
    
# Closing file
f.close()



new_dt670_b = dt670_b_4k_interp(new_x_list).round(4)

# output 
with open(r'C:\Users\rdm8\Documents\Modular_Cryostat_Stuff\dt670_b.json', 'w') as f:
    ujson.dump(new_dt670_b.tolist(), f)
    
# Closing file
f.close()



