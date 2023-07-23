import time
import board
import busio
import math
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class MQ4:
    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1115(i2c)
        self.ads.gain = 1

        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P0)

        # Create differential input between channel 0 and 1
        #chan = AnalogIn(ads, ADS.P0, ADS.P1)

        # Set the load resistance
        self.R0 = 4.55

    def voltage(self):
        return self.chan.voltage

    def ppm(self):
        RS_gas = ((5 * 1) / self.chan.voltage) - 1
        ratio = RS_gas / self.R0
        ppm = 1000*pow(ratio, -2.95)
        return ppm

# Create an instance of the MQ4 class
mq4 = MQ4()

while True:
    print("ppm: ", mq4.ppm(), "Voltage: ", mq4.voltage())
    time.sleep(1)

