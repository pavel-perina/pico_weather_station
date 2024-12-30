from machine import Pin, I2C
import time

def sht40_read(i2c):
    # Request raw temperature and humidity data
    i2c.writeto(0x44, bytes([0xfd]))
    time.sleep_ms(10)
    buffer = i2c.readfrom(0x44, 6)
    # Extract and convert temperature and humidity data
    temperature = (buffer[0] << 8) + buffer[1]
    humidity    = (buffer[3] << 8) + buffer[4]
    temperature = ((21875 * temperature) >> 13) - 45000
    humidity    = ((15625 * humidity) >> 13) - 6000
    return [temperature, humidity]

i2c = I2C(0, sda=Pin(0), scl=Pin(1))
while True:
    sht40_temp, sht40_rh = sht40_read(i2c)
    print(f"SHT40 temperature: {sht40_temp*.001:.2f}, humidity: {sht40_rh * .001:.2f}")
    time.sleep_ms(2000)