
class GlobalContext:
    """
    Global application context which stores various sensor data, event triggers...
    """
    def __init__(self, i2c, spi, ticks_ms:int):
        self.i2c = i2c
        self.spi = spi
        self.ticks_ms = ticks_ms
        self.sht40_temperature = 0.0
        self.sht40_humidity = 0.0
        self.sht40_valid = False # Not baking or cooling
        self.sht40_mock = True
        self.bmp280_temperature = 0.0
        self.bmp280_pressure = 0.0
        self.bmp280_mock = True
        self.backlight_percents = 0.0
        self.key_up_pressed = False
        self.key_down_pressed = False
        self.key_left_pressed = False
        self.key_right_pressed = False
        self.fb_width  = 84
        self.fb_height = 48
        self.framebuffer =  bytearray([0xAA] * (self.fb_width * self.fb_height // 8))
        self.framebuffer_dirty = False
        self.app = "SCREEN_MAIN"
