from machine import Pin, I2C
import time

def sht40_command(i2c, command):
    # Request raw temperature and humidity data
    time.sleep_ms(10)
    i2c.writeto(0x44, bytes([command]))
    time.sleep_ms(1200)
    buffer = i2c.readfrom(0x44, 6)
    # Extract and convert temperature and humidity data
    temperature = (buffer[0] << 8) + buffer[1]
    humidity    = (buffer[3] << 8) + buffer[4]
    temperature = ((21875 * temperature) >> 13) - 45000
    humidity    = ((15625 * humidity) >> 13) - 6000
    return [temperature, humidity]


i2c = I2C(0, sda=Pin(0), scl=Pin(1))
sht40_temp, sht40_rh = sht40_command(i2c, 0xfd)
i = 0
while i < 3600:
    command = 0xfd # Read
    if sht40_temp < 120*1000:
        command = 0x2f # 20mW
    if sht40_temp < 115*1000:
        command = 0x39 # 200mW
    sht40_temp, sht40_rh = sht40_command(i2c, command)
    print(f"{i:04d}, \"0x{command:02x}\", {sht40_temp*.001:.2f}, {sht40_rh * .001:.2f}")
    i += 1
