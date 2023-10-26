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
chan0 = AnalogIn(ads, ADS.P0)
#chan1 = AnalogIn(ads, ADS.P1)
# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))
RL = 1 #RL = 1kOhm
print("start calibrating...")
while True:
    #print("{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
    sensorVolt_chan0 = 0
    #sensorVolt_chan1 = 0
    for i in range(2):
        sensorVolt_chan0 += chan0.voltage
#        print(chan0.voltage)
        #sensorVolt_chan1 += chan1.voltage
#        print(chan1.voltage)
        time.sleep(1)
    sensorVolt_chan0 /= 2
    #sensorVolt_chan1 /= 50
    print("mean sensorVolt_chan0: ", sensorVolt_chan0)
    #print("mean sensorVolt_chan1: ", sensorVolt_chan1)
    RS_air_chan0 = ((5*RL) / sensorVolt_chan0) - RL
    #RS_air_chan1 = ((5*RL) / sensorVolt_chan1) - RL
    R0_chan0 = RS_air_chan0 / 4.4
    #R0_chan1 = RS_air_chan1 / 4.4
    print("R0_chan0: ", R0_chan0)
    #print("R0_chan1: ", R0_chan1)
    print("====================")
    time.sleep(1)
