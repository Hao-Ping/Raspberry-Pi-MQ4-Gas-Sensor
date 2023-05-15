import csv
import datetime
import time
import board
import busio
import math
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_sgp30
from sht20 import SHT20


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

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


##sht20
sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)
iaq_temp = sht.read_temp()
iaq_humid = sht.read_humid()

##sgp30
# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(celsius=iaq_temp, relative_humidity=iaq_humid)

elapsed_sec = 0


while True:
    #ch4
    RS_gas = ((5 * 1) / chan.voltage) - 1
    ratio = RS_gas / R0
    #ppm_log = (math.log(ratio, 10)- b) /m
    #ppm = pow(10, ppm_log)
    ppm = 1000*pow(ratio, -2.95)
    print("CH4 ppm: ", ppm, "Voltage: ", chan.voltage)

    #sht20
    temp = sht.read_temp()
    humid = sht.read_humid()
    print("Temp: ", temp, ", RH: ", humid)

    #sgp30
    eCO2 = sgp30.eCO2
    TVOC = sgp30.TVOC
    print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))
    time.sleep(1)
    elapsed_sec += 1
    if elapsed_sec > 0:
        elapsed_sec = 0
        sgp30.set_iaq_relative_humidity(celsius=temp, relative_humidity=humid)
        print(
            "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
            % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
        )

    

    with open('all_sensor_data.csv', 'a') as f:
        now = datetime.datetime.now()

        writer_object =csv.writer(f)
        writer_object.writerow([now.strftime('%Y/%m/%d %H:%M:%S'), ppm, chan.voltage, temp, humid, eCO2, TVOC])
        f.close()
    print("-------------------------------------------------")
    time.sleep(10)
