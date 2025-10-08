# SSD display initialization and loop
# Code proposed by Claude.AI / Sonnet 4.5
# Date: 2025-10-08

from machine import I2C
from global_context import GlobalContext

class Display:

    def __init(self, ctx):
        self.addr = 0x3C
        commands = [
            0xAE,       # Display off
            0x20, 0x00, # Memory addressing mode: horizontal
            0xB0,       # Page start address
            0xC0,       # COM scan direction (REVERSED - was 0xC8)
            0x00, 0x10, # Column start address
            0x40,       # Display start line
            0x81, 0xCF, # Contrast
            0xA0,       # Segment remap, either A0 or A1, one is upside down
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
            ctx.i2c.writeto(self.addr, bytes([0x00, cmd]))


    def on_tick(self, ctx):
        if ctx.framebuffer_dirty:
            ctx.i2c.writeto(self.addr, bytes([0, 0xB0])) # Page/Row 0
            ctx.i2c.writeto(self.addr, bytes([0, 0x00])) # Set column low nibble  ((column       & 0x0F)
            ctx.i2c.writeto(self.addr, bytes([0, 0x10])) # Set column high nibble ((column >> 4) & 0x0F)
            chunk_size = 32
            for i in range(0, ctx.fb_width * ctx.fb_height / 8, chunk_size)
                chunk = ctx.framebuffer[i:i+chunk_size]
                ctx.i2c.writeto(self.addr, bytes([0x40]) + chunk)
            ctx.framebuffer_dirty = False
