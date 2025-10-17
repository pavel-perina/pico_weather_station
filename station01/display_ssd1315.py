# SSD display initialization and loop
# Versions: 
# 2025-10-08 Code proposed by Claude.AI / Sonnet 4.5
# 2025-10-17 Code modified for SSD1315 display
# Date: 2025-10-08

from machine import I2C, Pin
from global_context import GlobalContext
import time

SSD1306_ADDR = 0x3C

# https://www.flowcode.co.uk/forums/viewtopic.php?t=3020
def display_init(i2c):
    print("ssd1315.display_init()")
    # NOTE: C0,A0 - up is cable side
    #       C8,A1 - up is pin side
    commands = [
            0xAE, # Display OFF
    0xD5, 0x80, # Clock
    0xA8, 0x3F, # Multiplex ratio (64 rows)
    0xD3, 0x00, # Offset
    0x40, # Start line at 0
    0x8D, 0x14, # Charge pump
    0x20, 0x00, # Horizontal addressing mode
    0xC0, # Scan direction
    0xA0, # Segment re-map
    0xDA, 0x12, # COM hardware config
    0x81, 0x7F, # Contrast
    0xD9, 0xF1, # Pre-charge
    0xDB, 0x40, # VCOMH deselect
    0xA4, # Entire display ON
    0xA6, # Normal display
    #0x21, 0x03, 0x82, # Column address range (shift +3)
    0x22, 0x00, 0x07, # Page address range (0-7)
    0xAF # Display ON
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
            chunk_size = 1024 #32
            for i in range(0, len(ctx.framebuffer), chunk_size):
                chunk = ctx.framebuffer[i:i+chunk_size]
                self.i2c.writeto(SSD1306_ADDR, bytes([0x40]) + chunk)
                #time.sleep_ms(5)
            ctx.framebuffer_dirty = False

if __name__ == "__main__":
    print("Running as standalone script")
    led = Pin("LED", Pin.OUT)
    led.toggle()
    i2c = I2C(1, sda=Pin(2), scl=Pin(3))
    display_init(i2c)
    reset_cursor(i2c)

    framebuffer = bytearray(b'\x00' * 1024)
    chunk_size = 32
    for i in range(0, len(framebuffer), chunk_size):
        chunk = framebuffer[i:i+chunk_size]
        i2c.writeto(SSD1306_ADDR, bytes([0x40]) + chunk)
        time.sleep_ms(5)

    # Smiley 10x8 pixels
    buffer = bytes([0x3c, 0x42, 0x81, 0x95, 0xa1, 0xa1, 0x95, 0x81, 0x42, 0x3c ])
    i2c.writeto(SSD1306_ADDR, bytes([0x40]) + buffer)
    print("All done, display should be happy")
