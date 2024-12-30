import pcd8544
from machine import Pin, SPI
import sys
from utime import sleep_ms
# Load font file
font_8x6 = bytearray(6*256)
with open("/font-6x8.bin", "rb") as file:
  n_read = file.readinto(font_8x6)
  assert(n_read == 6*256)
# Initialize SPI display
spi = SPI(1, baudrate=1000000, mosi=Pin(11), sck=Pin(10))
lcd = pcd8544.PCD8544(spi, cs = Pin(18), dc = Pin(16), rst = Pin(17))
lcd.clear()
sleep_ms(200)
# Display text
for row, text in enumerate([
    "\x10Hello world!\x02",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmn", 
    "opqrstuvwxyz",
    "\xDB\xDB\xDB\xB2\xB1\xB0\xB0\x10", 
    "The last row .>"]):
  lcd.position(0, row)
  for ch in text:
    start_index = ord(ch)*6
    glyph = font_8x6[start_index:start_index+6]
    lcd.data(glyph)
    sleep_ms(20)

print("DONE.")



    
