# SSD display initialization and loop
# Versions: 
# 2025-10-08 Code proposed by Claude.AI / Sonnet 4.5
# 2025-10-17 Code modified for SSD1315 display (works with both)

from machine import I2C, Pin
from global_context import GlobalContext
import time

SSD1306_ADDR = 0x3C
# Note: second one works
# https://www.flowcode.co.uk/forums/viewtopic.php?t=3020
# https://bitbucket.org/tinusaur/ssd1306xled/src/master/ssd1306xled/ssd1306xled.c
def display_init(i2c):
    print("ssd1306.display_init()")
    # NOTE: C0,A0 - up is cable side
    #       C8,A1 - up is pin side
    commands = [
        0xAE,           # Set Display ON/OFF - AE=OFF, AF=ON
        0xD5, 0xF0,		# Set display clock divide ratio/oscillator frequency, set divide ratio
        0xA8, 0x3F,		# Set multiplex ratio (1 to 64) ... (height - 1)
        0xD3, 0x00,		# Set display offset. 00 = no offset
        0x40 | 0x00,	# Set start line address, at 0.
        0x8D, 0x14,		# Charge Pump Setting, 14h = Enable Charge Pump
        0x20, 0x00,		# Set Memory Addressing Mode - 00=Horizontal, 01=Vertical, 10=Page, 11=Invalid
        0xA0 | 0x00,	# Set Segment Re-map
        0xC0,			# Set COM Output Scan Direction
        0xDA, 0x12,		# Set COM Pins Hardware Configuration - 128x32:0x02, 128x64:0x12
        0x81, 0x3F,		# Set contrast control register
        0xD9, 0xF1,		# Set pre-charge period (0x22 or 0xF1)
        0xDB, 0x30,		# Set Vcomh Deselect Level - 0x00: 0.65 x VCC, 0x20: 0.77 x VCC (RESET), 0x30: 0.83 x VCC
        0xA4,			# Entire Display ON (resume) - output RAM to display
        0xA6,			# Set Normal/Inverse Display mode. A6=Normal; A7=Inverse
        0x2E,			# Deactivate Scroll command
        0x22, 0x00, 0x3f,	# Set Page Address (start,end)
        0x21, 0x00,	0x7f,	# Set Column Address (start,end)
        0xAF,			# Set Display ON/OFF - AE=OFF, AF=ON
    ]

    for cmd in commands:
        i2c.writeto(SSD1306_ADDR, bytes([0x00, cmd]))
        
def reset_cursor(i2c):
    i2c.writeto(SSD1306_ADDR, bytes([0, 0xB0])) # Page/Row 0
    i2c.writeto(SSD1306_ADDR, bytes([0, 0x00])) # Set column low nibble  ((column       & 0x0F)
    i2c.writeto(SSD1306_ADDR, bytes([0, 0x10])) # Set column high nibble ((column >> 4) & 0x0F)

class Display:

    def __init__(self, ctx):
        self.i2c = ctx.i2c_disp
        display_init(self.i2c)

    def on_tick(self, ctx):
        if ctx.framebuffer_dirty:
            reset_cursor(self.i2c)
            chunk_size = 32 # Note: even 1024 works
            for i in range(0, len(ctx.framebuffer), chunk_size):
                chunk = ctx.framebuffer[i:i+chunk_size]
                self.i2c.writeto(SSD1306_ADDR, bytes([0x40]) + chunk)
            ctx.framebuffer_dirty = False

if __name__ == "__main__":
    print("Running as standalone script")
    led = Pin("LED", Pin.OUT)
    led.toggle()
    i2c = I2C(0, sda=Pin(0), scl=Pin(1))
    display_init(i2c)
    reset_cursor(i2c)

    framebuffer = bytearray(b'\x00' * 1024)
    chunk_size = 32
    for i in range(0, len(framebuffer), chunk_size):
        chunk = framebuffer[i:i+chunk_size]
        i2c.writeto(SSD1306_ADDR, bytes([0x40]) + chunk)

    # Smiley 10x8 pixels
    buffer = bytes([0x3c, 0x42, 0x81, 0x95, 0xa1, 0xa1, 0x95, 0x81, 0x42, 0x3c ])
    i2c.writeto(SSD1306_ADDR, bytes([0x40]) + buffer)
    print("All done, display should be happy")
