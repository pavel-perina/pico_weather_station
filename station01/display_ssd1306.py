# SSD display initialization and loop
# Code proposed by Claude.AI / Sonnet 4.5
# Date: 2025-10-08

from machine import I2C, Pin
from global_context import GlobalContext
import time

SSD1306_ADDR = 0x3C

def display_init(i2c):
    print("ssd1306.display_init()")
    # NOTE: C0,A0 - up is cable side
    #       C8,A1 - up is pin side
    commands = [
        0xAE,       # Display off
        0x20, 0x00, # Memory addressing mode: horizontal
        0xB0,       # Page start address
        0xC0,       # COM scan direction (upside-down flip C8 or C0)
        0x00, 0x10, # Column start address
        0x40,       # Display start line
        0x81, 0xCF, # Contrast
        0xA0,       # Segment remap, either A0 or A1, left-right flip
        0xA6,       # Normal display
        0xA8, 0x3F, # Multiplex ratio (64-1)
        0xD3, 0x00, # Display offset
        0xD5, 0x80, # Clock divide ratio
        0xD9, 0xF1, # Pre-charge period
        0xDA, 0x12, # COM pins configuration
        0xDB, 0x40, # VCOM deselect level
        0x8D, 0x14, # Charge pump
        0xAF        # Display on
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
            chunk_size = 32
            for i in range(0, len(ctx.framebuffer), chunk_size):
                chunk = ctx.framebuffer[i:i+chunk_size]
                self.i2c.writeto(SSD1306_ADDR, bytes([0x40]) + chunk)
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

    # Smiley 10x8 pixels
    buffer = bytes([0x3c, 0x42, 0x81, 0x95, 0xa1, 0xa1, 0x95, 0x81, 0x42, 0x3c ])
    i2c.writeto(SSD1306_ADDR, bytes([0x40]) + buffer)
