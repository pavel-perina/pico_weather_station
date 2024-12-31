import time
from machine import I2C
from global_context import GlobalContext

class Sht40:

    def __init__(self):
        # awaitin data
        self.awaiting_data_since_ticks = 0
        self.last_update_ticks = 0
        self.is_baking = False
        self.i2c_addr = 0x44
        self.command = 0
        self.last_baking = 0

    def on_tick(self, ctx:GlobalContext):
        if (self.awaiting_data_since_ticks > 0): 
            if (ctx.ticks_ms - self.awaiting_data_since_ticks) >= 10:
                if self.is_baking:
                    self.last_baking = ctx.ticks_ms
                buffer = ctx.i2c.readfrom(self.i2c_addr, 6)
                # Extract and convert temperature and humidity data
                temperature = (buffer[0] << 8) + buffer[1]
                humidity    = (buffer[3] << 8) + buffer[4]
                ctx.sht40_temperature = ((21875 * temperature) >> 13) - 45000
                ctx.sht40_humidity    = ((15625 * humidity) >> 13) - 6000
                ctx.sht40_valid       = ((ctx.ticks_ms - self.last_baking) > 5*60*1000)
                self.awaiting_data_since_ticks  = 0
                self.last_update_ticks          = ctx.ticks_ms 
        else:
            if (ctx.ticks_ms - self.last_update_ticks) > 1000:
                self.command = 0xfd if not self.is_baking else 0x39
                ctx.i2c.writeto(self.i2c_addr, bytes([self.command]))
                self.awaiting_data_since_ticks = ctx.ticks_ms
    