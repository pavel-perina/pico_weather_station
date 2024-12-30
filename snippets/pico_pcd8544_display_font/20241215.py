import pcd8544
from machine import Pin, SPI, I2C
import sys
from utime import sleep_ms

def sht40_read(i2c):
    # Request raw temperature and humidity data
    i2c.writeto(0x44, bytes([0xfd]))
    sleep_ms(10)
    buffer = i2c.readfrom(0x44, 6)
    # Extract and convert temperature and humidity data
    temperature = (buffer[0] << 8) + buffer[1]
    humidity    = (buffer[3] << 8) + buffer[4]
    temperature = ((21875 * temperature) >> 13) - 45000
    humidity    = ((15625 * humidity) >> 13) - 6000
    return [temperature, humidity]


# Load font file
font_8x6 = bytearray(6*256)
with open("/font-6x8.bin", "rb") as file:
  n_read = file.readinto(font_8x6)
  assert(n_read == 6*256)

# Initialize SPI display
spi = SPI(1, baudrate=1000000, mosi=Pin(11), sck=Pin(10))
lcd = pcd8544.PCD8544(spi, cs = Pin(18), dc = Pin(16), rst = Pin(17))
lcd.clear()
sleep_ms(1000)

i2c = I2C(0, sda=Pin(0), scl=Pin(1))


while True:
    sht40_temp, sht40_rh = sht40_read(i2c)

    # Display text
    for row, text in enumerate([
        "Raspberry Pico",
        "--------------",
        "Screen:PCD8544",
        "Sensor:  SHT40",
        f"Temp:  {sht40_temp*0.001:3.2f}\xf8C",
        f"RH:     {sht40_rh*0.001:2.2f}%",
    ]):
        lcd.position(0, row)
        for ch in text:
            start_index = ord(ch)*6
            glyph = font_8x6[start_index:start_index+6]
            lcd.data(glyph)
    sleep_ms(1000)


    
