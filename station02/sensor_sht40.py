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
            if time.ticks_diff(ctx.ticks_ms, self.awaiting_data_since_ticks) >= 10:
                if self.is_baking:
                    self.last_baking = ctx.ticks_ms
                buffer = ctx.i2c.readfrom(self.i2c_addr, 6)
                # Extract and convert temperature and humidity data
                temperature = (buffer[0] << 8) + buffer[1]
                humidity    = (buffer[3] << 8) + buffer[4]
                ctx.sht40_temperature = ((21875 * temperature) >> 13) - 45000
                ctx.sht40_humidity    = ((15625 * humidity) >> 13) - 6000
                ctx.sht40_temperature *= 0.001
                ctx.sht40_humidity    *= 0.001
                ctx.sht40_valid       = ((ctx.ticks_ms - self.last_baking) > 5*60*1000)
                self.awaiting_data_since_ticks  = 0
                self.last_update_ticks          = ctx.ticks_ms 
        else:
            if time.ticks_diff(ctx.ticks_ms, self.last_update_ticks) > 1000:
                self.command = 0xfd if not self.is_baking else 0x39
                ctx.i2c.writeto(self.i2c_addr, bytes([self.command]))
                self.awaiting_data_since_ticks = ctx.ticks_ms

if __name__ == "__main__":
    print("Running as standalone script")

    import struct
    from machine import Pin, I2C
    #i2c = I2C(0, sda=Pin(16), scl=Pin(17)) #does not work, SoftI2C does
    i2c = I2C(0, sda=Pin(0), scl=Pin(1))

    print(i2c.scan())

    buffer=bytearray(6)
    buffer[0]= 0xfd
    i2c.writeto(68, buffer)
    buffer=i2c.readfrom(68, 6)
    temp_data = buffer[0:2]
    temperature = struct.unpack_from(">H", temp_data)[0]
    temperature = -45.0 + 175.0 * temperature / 65535.0
    print(temperature)
    humidity_data = buffer[3:5]
    humidity = struct.unpack_from(">H", humidity_data)[0]
    humidity = -6.0 + 125.0 * humidity / 65535.0
    print(humidity)
