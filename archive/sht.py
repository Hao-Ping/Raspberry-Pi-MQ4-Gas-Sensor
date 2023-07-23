from sht20 import SHT20
import time

sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)

while True:
    temp = sht.read_temp()
    humid = sht.read_humid()

    print("Temp: ", temp, ", RH: ", humid)
    time.sleep(5)
