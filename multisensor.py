from datetime import datetime
import time
import board
import busio
import math
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_sgp30
from sht20 import SHT20

class MQ5GasSensor:
    def __init__(self, channel, R0=10.05):
        #self.ads = ads
        self.channel = channel
        self.R0 = R0

    def read_ppm(self):
        voltage = self.channel.voltage
        RS_gas = ((5 * 1) / voltage) - 1
        ratio = RS_gas / self.R0
        ppm = 1000 * pow(ratio, -2.95)
        return ppm, voltage

class SHT20Sensor:
    def __init__(self):
        self.sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)

    def read_temperature(self):
        return self.sht.read_temp()

    def read_humidity(self):
        return self.sht.read_humid()

class SGP30GasSensor:
    def __init__(self, i2c):
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

    def initialize(self, temperature, humidity):
        self.sgp30.set_iaq_baseline(0x8973, 0x8AAE)
        self.sgp30.set_iaq_relative_humidity(celsius=temperature, relative_humidity=humidity)

    def read_eCO2_TVOC(self):
        self.elapsed_sec = 0
        return self.sgp30.eCO2, self.sgp30.TVOC
    
    
    # def set_elapsed_time(self, time=0):
    #     self.elapsed_time = time
    
    def self_calibration(self, temperature, humidity):
        time.sleep(1)
        self.elapsed_sec += 1
        if self.elapsed_sec > 0:
            self.elapsed_sec = 0
            self.sgp30.set_iaq_relative_humidity(celsius=temperature, relative_humidity=humidity)
            print(
                "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                % (self.sgp30.baseline_eCO2, self.sgp30.baseline_TVOC)
            )

    
if __name__ == "__main__":
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    ads = ADS.ADS1115(i2c)
    ads.gain = 1
    chan = AnalogIn(ads, ADS.P0)

    mq5_sensor = MQ5GasSensor(chan)
    sht20_sensor = SHT20Sensor()
    sgp30_sensor = SGP30GasSensor(i2c)

    print("SGP30 serial #", [hex(i) for i in sgp30_sensor.sgp30.serial])
    sgp30_sensor.initialize(sht20_sensor.read_temperature(), sht20_sensor.read_humidity())


    while True:
        ppm, voltage = mq5_sensor.read_ppm()
        print("CH4 ppm:", ppm, "Voltage:", voltage)

        temperature = sht20_sensor.read_temperature()
        humidity = sht20_sensor.read_humidity()
        print("Temp:", temperature, "RH:", humidity)

        eCO2, TVOC = sgp30_sensor.read_eCO2_TVOC()
        print("eCO2 =", eCO2, "ppm, TVOC =", TVOC, "ppb")

        sgp30_sensor.self_calibration(temperature, humidity)

        print("-------------------------------------------------")
        time.sleep(30)
