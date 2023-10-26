import time
import board
import busio
import math
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 1

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)
# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))
#m = -0.350
#b = 2.417
R0 = 5

while True:
    RS_gas_0 = ((5 * 1) / chan0.voltage) - 1
    ratio_0 = RS_gas_0 / R0
    RS_gas_1 = ((5 * 1) / chan1.voltage) - 1
    ratio_1 = RS_gas_1 / R0
    RS_gas_2 = ((5 * 1) / chan2.voltage) - 1
    ratio_2 = RS_gas_2 / R0
    RS_gas_3 = ((5 * 1) / chan3.voltage) - 1
    ratio_3 = RS_gas_3 / R0
    #ppm_log = (math.log(ratio, 10)- b) /m
    #ppm = pow(10, ppm_log)
    #ppm = 1000*pow(ratio, -2.95)
    #print("ppm: ", ppm, "Voltage: ", chan.voltage)
    print("chan0: ", chan0.voltage)
    print("chan1: ", chan1.voltage)
    print("chan2: ", chan2.voltage)
    print("chan3: ", chan3.voltage)
    print("===========")
    time.sleep(3)
