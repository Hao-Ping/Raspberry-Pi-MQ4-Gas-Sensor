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


while True:
    #ch4
    RS_gas_chan0 = ((5 * 1) / chan0.voltage) - 1
    #RS_gas_chan1 = ((5 * 1) / chan1.voltage) - 1
    ratio_chan0 = RS_gas_chan0 / R0_chan0
    #ratio_chan1 = RS_gas_chan1 / R0_chan1
    #ppm_log = (math.log(ratio, 10)- b) /m
    #ppm= pow(10, ppm_log)
    ppm_chan0 = 1000*pow(ratio_chan0, -2.95)
    #ppm_chan1 = 1000*pow(ratio_chan1, -2.95)
    print("chan0 CH4 ppm: ", ppm_chan0, "Voltage: ", chan0.voltage)
    #print("chan1 CH4 ppm: ", ppm_chan1, "Voltage: ", chan1.voltage)

    #sht20
    #temp = sht.read_temp()
    #humid = sht.read_humid()
    #print("Temp: ", temp, ", RH: ", humid)

    #sgp30
    #eCO2 = sgp30.eCO2
    #TVOC = sgp30.TVOC
    #print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))
    #time.sleep(1)
    #elapsed_sec += 1
    #if elapsed_sec > 0:
    #    elapsed_sec = 0
    #    sgp30.set_iaq_relative_humidity(celsius=temp, relative_humidity=humid)
    #    print(
    #        "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
    #        % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
    #    )

    

    with open('/home/pi/Raspberry-Pi-MQ4-Gas-Sensor/ch4_data_20230813.csv', 'a') as f:
        now = datetime.datetime.now()

        writer_object =csv.writer(f)
        writer_object.writerow([now.strftime('%Y/%m/%d %H:%M:%S'),"chan0", ppm_chan0, chan0.voltage])
        #writer_object.writerow([now.strftime('%Y/%m/%d %H:%M:%S'),"chan1", ppm_chan1, chan1.voltage])
        f.close()
    print("-------------------------------------------------")
    time.sleep(1)
