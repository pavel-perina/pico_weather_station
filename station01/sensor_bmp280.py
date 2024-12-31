import time
from machine import I2C
import struct
from global_context import GlobalContext


REG_CALIB_DATA  = 0x88
REG_CHIP_ID     = 0xD0
REG_RESET       = 0xE0
REG_CTRL_MEAS   = 0xF4
REG_CONFIG      = 0xF5
REG_PRESS_MSB   = 0xF7

def decode_20bit(data: bytes) -> int:
    return (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)  

class Bmp280Calibration:
    def __init__(self, T1=0, T2=0, T3=0, P1=0, P2=0, P3=0, P4=0, P5=0, P6=0, P7=0, P8=0, P9=0, H1=0):
        self.T1 = T1
        self.T2 = T2
        self.T3 = T3
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4
        self.P5 = P5
        self.P6 = P6
        self.P7 = P7
        self.P8 = P8
        self.P9 = P9
        self.H1 = H1
    def from_bytes(self, cal_data: bytes):
        # Format: <HHHHHHHHHHHH
        # < = little endian, H = uint16
        values = struct.unpack('<HHHHHHHHHHHH', cal_data[:24])
        self.T1=values[0]
        self.T2=struct.unpack('<h', struct.pack('<H', values[1]))[0]  # Convert to signed
        self.T3=struct.unpack('<h', struct.pack('<H', values[2]))[0]
        self.P1=values[3]
        self.P2=struct.unpack('<h', struct.pack('<H', values[4]))[0]
        self.P3=struct.unpack('<h', struct.pack('<H', values[5]))[0]
        self.P4=struct.unpack('<h', struct.pack('<H', values[6]))[0]
        self.P5=struct.unpack('<h', struct.pack('<H', values[7]))[0]
        self.P6=struct.unpack('<h', struct.pack('<H', values[8]))[0]
        self.P7=struct.unpack('<h', struct.pack('<H', values[9]))[0]
        self.P8=struct.unpack('<h', struct.pack('<H', values[10]))[0]
        self.P9=struct.unpack('<h', struct.pack('<H', values[11]))[0]
        self.H1=cal_data[25]

    def decode_measurement(self, meas_data: bytes):
        hex_string = ' '.join(f'{byte:02x}' for byte in meas_data)
        print("Raw measurement: "+hex_string)
        # Temperature
        temp_raw = decode_20bit(meas_data[3:6])
        var1 = ((temp_raw >> 3) - (self.T1 << 1)) * self.T2 >> 11
        var2 = (((temp_raw >> 4) - self.T1) * ((temp_raw >> 4) - self.T1) >> 12) * self.T3 >> 14
        t_fine = var1 + var2
        T = (t_fine * 5 + 128) >> 8

        # Pressure
        adc_P = decode_20bit(meas_data[0:3])
        var1 = t_fine - 128000
        var2 = var1 * var1 * self.P6
        var2 = var2 + ((var1 * self.P5) << 17)
        var2 = var2 + (self.P4 << 35)
        var1 = ((var1 * var1 * self.P3) >> 8) + ((var1 * self.P2) << 12)
        var1 = ((1 << 47) + var1) * self.P1 >> 33
        
        if var1 != 0:
            p = 1048576 - adc_P
            p = ((p << 31) - var2) * 3125 // var1
            var1 = (self.P9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (self.P8 * p) >> 19
            p = ((p + var1 + var2) >> 8) + (self.P7 << 4)

        return (T / 100.0, p / 256.0)


class Bmp280:

    def __init__(self, ctx:GlobalContext):
        # awaiting data
        print("Initializing BMP280")
        self.awaiting_data_since_ticks = 0
        self.last_update_ticks = 0
        self.i2c_addr = 0x76
        # Reset 
        ctx.i2c.writeto(self.i2c_addr, bytes([REG_RESET, 0xB6]))
        time.sleep_ms(50)
        # Read calibration
        self.calibration = Bmp280Calibration()
        ctx.i2c.writeto(self.i2c_addr, bytes([REG_CALIB_DATA]))
        time.sleep_ms(50)
        raw_calibration = ctx.i2c.readfrom(self.i2c_addr, 26)
        self.calibration.from_bytes(raw_calibration)
        time.sleep_ms(50)
        hex_string = ' '.join(f'{byte:02x}' for byte in raw_calibration)
        print("Raw calibration: " + hex_string)
        # Write config and control registers
        ctx.i2c.writeto(self.i2c_addr, bytes([REG_CTRL_MEAS, 0x27]))
        time.sleep_ms(50)
        ctx.i2c.writeto(self.i2c_addr, bytes([REG_CONFIG, 0x00]))
        time.sleep_ms(50)

        
    def on_tick(self, ctx:GlobalContext):
        if (self.awaiting_data_since_ticks > 0): 
            if (ctx.ticks_ms - self.awaiting_data_since_ticks) >= 50:
                buffer = ctx.i2c.readfrom(self.i2c_addr, 6)
                (ctx.bmp280_temperature, ctx.bmp280_pressure) = self.calibration.decode_measurement(buffer)
                self.awaiting_data_since_ticks  = 0
                self.last_update_ticks          = ctx.ticks_ms 
        else:
            if (ctx.ticks_ms - self.last_update_ticks) > 1000:
                ctx.i2c.writeto(self.i2c_addr, bytes([REG_PRESS_MSB]))
                self.awaiting_data_since_ticks = ctx.ticks_ms
    
if __name__ == "__main__":
    # This block will only run if the file is executed as a standalone script
    print("Running as standalone script")
    calib_data = bytearray(b'\x5e\x6d\x07\x68\x18\xfc\x01\x93\xf5\xd5\xd0\x0b\xb2\x08\xbe\x00\xf9\xff\x8c\x3c\xf8\xc6\x70\x17\x00\x00')
    meas_data  = bytearray(b'\x5d\x3b\x00\x6d\x67\x00')
    calib = Bmp280Calibration()
    calib.from_bytes(calib_data)
    (temp, pressure) = calib.decode_measurement(meas_data)
    print(f"Temp: {temp}, Pressure: {pressure}")
    
else:
    # This block will run if the file is imported as a module
    from machine import I2C