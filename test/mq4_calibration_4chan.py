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
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)
# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))
RL = 1 #RL = 1kOhm
print("start calibrating...")
while True:
    #print("{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
    sensorVolt_chan0 = 0
    sensorVolt_chan1 = 0
    sensorVolt_chan2 = 0
    sensorVolt_chan3 = 0

    for i in range(2):
        sensorVolt_chan0 += chan0.voltage
#        print(chan0.voltage)
        sensorVolt_chan1 += chan1.voltage
#        print(chan1.voltage)
        sensorVolt_chan2 += chan2.voltage
        sensorVolt_chan3 += chan3.voltage
        time.sleep(1)
    sensorVolt_chan0 /= 2
    sensorVolt_chan1 /= 2
    sensorVolt_chan2 /= 2
    sensorVolt_chan3 /= 2
    print("mean sensorVolt_chan0: ", sensorVolt_chan0)
    print("mean sensorVolt_chan1: ", sensorVolt_chan1)
    print("mean sensorVolt_chan2: ", sensorVolt_chan2)
    print("mean sensorVolt_chan3: ", sensorVolt_chan3)

    RS_air_chan0 = ((5*RL) / sensorVolt_chan0) - RL
    RS_air_chan1 = ((5*RL) / sensorVolt_chan1) - RL
    RS_air_chan2 = ((5*RL) / sensorVolt_chan2) - RL
    RS_air_chan3 = ((5*RL) / sensorVolt_chan3) - RL
    
    R0_chan0 = RS_air_chan0 / 4.4
    R0_chan1 = RS_air_chan1 / 4.4
    R0_chan2 = RS_air_chan2 / 4.4
    R0_chan3 = RS_air_chan3 / 4.4



    print("R0_chan0: ", R0_chan0)
    print("R0_chan1: ", R0_chan1)
    print("R0_chan2: ", R0_chan2)
    print("R0_chan3: ", R0_chan3)
    print("====================")
    time.sleep(1)
