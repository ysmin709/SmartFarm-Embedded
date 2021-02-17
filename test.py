#!/usr/bin/python

import io
import sys
import fcntl
import time
import datetime
import pytz
import copy
import string
import os
from Data import (
    Data
)
from AtlasI2C import (
	 AtlasI2C
)
    
def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
    
    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        moduletype = response.split(",")[1] 
        response = device.query("name,?").split(",")[1]
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list
       

def main():
    
    device_list = get_devices()
        
    device = device_list[0]
    
    real_raw_input = vars(__builtins__).get('raw_input', input)
    
    data = Data()
    
    while True:
        user_cmd = 'poll'
        
        cmd_list = user_cmd.split(',')
        if len(cmd_list) > 1:
            delaytime = float(cmd_list[1])
        else:
            delaytime = device.long_timeout
       
        # check for polling time being too short, change it to the minimum timeout if too short
        if delaytime < device.long_timeout:
            print("Polling time is shorter than timeout, setting polling time to %0.2f" % device.long_timeout)
            delaytime = device.long_timeout
        try:
            while True:    
                data_list = []
                for dev in device_list:
                    dev.write("R")
                time.sleep(delaytime)
                for dev in device_list:
                    temp = dev.read()
                    temp1 = temp.split(' ')
                    status = temp[0] # check success or error
                    temp2 = temp1[4].split('\x00')
                    data_list.append(temp2[0])
                print(data_list)
                if status is "Error":
                    data.update(error=True)
                    data.error_post()
                else:
                    data.ph = float(data_list[0])
                    data.ec = round(float(data_list[1]) / 1000, 2)
                    data.rtd = round(float(data_list[2]), 1)
                    #data.pmp = round(float(data_list[3]), 1)
                    data.co2 = round(float(data_list[3]), 1)
                    data.hum = round(float(data_list[4]), 1)
                    
                    data.checkRecipe(data.ph, data.ec, data.rtd, data.co2, data.hum)
                time.sleep(58.75)
            
        except KeyboardInterrupt:       # catches the ctrl-c command, which breaks the loop above
            print("Continuous polling stopped")
            print_devices(device_list, device)
            

                    
if __name__ == '__main__':
    main()


