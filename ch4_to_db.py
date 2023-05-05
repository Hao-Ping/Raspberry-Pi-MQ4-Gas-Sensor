import sql
import csv

import time
import board
import busio
import math
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

db_connected = False
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 1

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))
#m = -0.350
#b = 2.417
R0 = 4.55

while True:
    try:
        RS_gas = ((5 * 1) / chan.voltage) - 1
        ratio = RS_gas / R0
        #ppm_log = (math.log(ratio, 10)- b) /m
        #ppm = pow(10, ppm_log)
        ppm = 1000*pow(ratio, -2.95)
        print("ppm: ", ppm, "Voltage: ", chan.voltage)

        if sql.wifi_is_connected():
            if db_connected == False:
                curr_db = sql.connect_db()
                db_connected = True
            
            # # Read and resend lost data to db
            # with open('lost_data_backup.csv','r') as f:
            #     rows = csv.reader(f)
            #     for data_row in rows:
            #         sql.write_data_to_db(curr_db, data_row[2], data_row[0], data_row[1])
            # Clear lost data file
            # with open('lost_data_backup.csv','w') as f:
            #     pass
            
            # Write current data to db
            # for data_row in csv_data:
            #     sql.write_data_to_db(curr_db, data_row[2], data_row[0], data_row[1])
            sql.write_data_to_db(curr_db, ppm, chan.voltage)
        # else:
        #     db_connected = False
        #     with open('lost_data_backup.csv', 'a') as f:
        #             write = csv.writer(f)
        #             write.writerows(csv_data)

        time.sleep(5)
    except Exception as e:
        dataFromSD = "" # Initialize
        # try:
        #     p = 0
        #     while p == 0:
        #         if p != 0:
        #             continue
        #         p = btle.Peripheral(blue_address)
        #         p.withDelegate(ReadDelegate())
        #         sdName = shadowName
        #         # Initialize, four variables
        #         message_flag2 = 0
        #         AWS_flag_1 = 1
        #         AWS_flag_2 = 0
        #         temp = None
        #         mois = None
        #         vwc = None
        #         ec = None
        #         light = None
        
        # # Close db connection if Keyboard Interrupt or other error
        sql.disconnect_db(curr_db)
