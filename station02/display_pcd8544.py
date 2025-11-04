from machine import SPI, Pin
import pcd8544

class Display:

    def __init__(self, ctx):
        #self.lcd = pcd8544.PCD8544(ctx.spi, cs = Pin(18), dc = Pin(16), rst = Pin(17))
        #self.lcd.clear()
        pass

    def on_tick(self, ctx):
        #if ctx.framebuffer_dirty:
        #    self.lcd.position(0,0)
        #    self.lcd.data(ctx.framebuffer)
        #    ctx.framebuffer_dirty = False
        pass
