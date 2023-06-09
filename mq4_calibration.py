import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 1 # Full-scale Range +/- 4.096V

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))
RL = 1 #RL = 1kOhm
while True:
    #print("{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
    sensorVolt = 0
    for i in range(500):
        sensorVolt += chan.voltage
    sensorVolt /= 500
    print("mean sensorVolt: ", sensorVolt)
    RS_air = ((5*RL) / sensorVolt) - RL
    R0 = RS_air / 4.4
    print("R0: ", R0)
    time.sleep(1)
