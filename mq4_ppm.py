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
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))
m = -0.350
b = 2.417
R0 = 3.5

while True:
    RS_gas = ((5 * 1) / chan.voltage) - 1
    ratio = RS_gas / R0
    #ppm_log = (math.log(ratio, 10)- b) /m
    #ppm = pow(10, ppm_log)
    ppm = 1000*pow(ratio, -2.95)
    print("ppm: ", ppm)
    time.sleep(1)
