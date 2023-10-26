import csv
import datetime
import time
import board
import busio
import math
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#import adafruit_sgp30
#from sht20 import SHT20


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 1

# Create single-ended input on chan0nel 0
chan0 = AnalogIn(ads, ADS.P0)
# chan1 = AnalogIn(ads, ADS.P1)
# Create differential input between chan0nel 0 and 1
#chan0 = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))
#m = -0.350
#b = 2.417
R0_chan0 = 7.90
# R0_chan1 = 4.75

##sht20
#sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)
#iaq_temp = sht.read_temp()
#iaq_humid = sht.read_humid()

##sgp30
# Create library object on our I2C port
#sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

#print("SGP30 serial #", [hex(i) for i in sgp30.serial])

#sgp30.set_iaq_baseline(0x8973, 0x8AAE)
#sgp30.set_iaq_relative_humidity(celsius=iaq_temp, relative_humidity=iaq_humid)

#elapsed_sec = 0




def collect_data(start_time, end_time, interval, filename):
    counter = 0 
    while True:
        now = datetime.datetime.now()
        current_time = now.time()
        
        RS_gas_chan0 = ((5 * 1) / chan0.voltage) - 1
        ratio_chan0 = RS_gas_chan0 / R0_chan0
        ppm_chan0 = 1000 * pow(ratio_chan0, -2.95)
        print("chan0 CH4 ppm:", ppm_chan0, "Voltage:", chan0.voltage)
        print("-------------------------------------------------")

        # Adjust hour for the afternoon period
        if current_time >= datetime.time(12, 0) and current_time <= datetime.time(23, 59, 59):
            current_hour = current_time.hour - 12
        else:
            current_hour = current_time.hour
            
        if start_time <= current_hour and current_hour <= end_time:
            with open(filename, 'a') as f:
                writer_object = csv.writer(f)
                writer_object.writerow([now.strftime('%Y/%m/%d %H:%M:%S'), "chan0", ppm_chan0, chan0.voltage])
        else: 
            counter += 1
            print(counter)
            if counter == 100:
                with open(filename, 'a') as f:
                    writer_object = csv.writer(f)
                    writer_object.writerow([now.strftime('%Y/%m/%d %H:%M:%S'), "chan0", ppm_chan0, chan0.voltage])
                    counter = 0
            
        time.sleep(interval)

# Define the time ranges and interval
start_time = 4
end_time = 7
interval = 3  # seconds

# Replace 'your_filename.csv' with the actual filename
filename = '/home/pi/Raspberry-Pi-MQ4-Gas-Sensor/ch4_data_20230813.csv'

# Call the function for both morning and evening periods
collect_data(start_time, end_time, interval, filename)
