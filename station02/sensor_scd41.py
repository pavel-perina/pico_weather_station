# Sensirion SCD41 (temp, humidity, co2) driver
# Date: 2025-10-08
#
# Datasheet:
# https://sensirion.com/media/documents/48C4B7FB/67FE0194/CD_DS_SCD4x_Datasheet_D1.pdf

# TODO: temperature offset
from machine import I2C
from global_context import GlobalContext
import time

SCD41_ADDR = 0x62 # 98

def crc8(data):
    """Calculate CRC-8 checksum for Sensirion sensors"""
    crc = 0xFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = crc << 1
    return crc & 0xFF

def decode_measurement(buffer):
    # Verify CRCs (every 2 bytes followed by 1 CRC byte)
    if crc8(buffer[0:2]) != buffer[2]:
        print("CRC error on CO2")
        return None
    if crc8(buffer[3:5]) != buffer[5]:
        print("CRC error on temperature")
        return None
    if crc8(buffer[6:8]) != buffer[8]:
        print("CRC error on humidity")
        return None
        
    co2ppm = (buffer[0] << 8) | buffer[1]
    temperature = (buffer[3] << 8) + buffer[4]
    temperature = ((21875 * temperature) >> 13) - 45000
    temperature = temperature * 0.001
    humidity = (buffer[6] << 8) | buffer[7]
    humidity = (12500*humidity) >> 13
    humidity = humidity * 0.001
    return [temperature, humidity, co2ppm]

def scd41_init(i2c):
    # Stop any periodic measurement first
    try:
        i2c.writeto(SCD41_ADDR, bytes([0x3F, 0x86]))
        time.sleep_ms(500)
    except:
        pass

    # Start periodic measurement
    i2c.writeto(SCD41_ADDR, bytes([0x21, 0xB1]))
    time.sleep_ms(1000)



def scd41_measure(i2c):
    # get_data_ready_status
    i2c.writeto(SCD41_ADDR, bytes([0xE4, 0xB8]))
    time.sleep_ms(1)
    buffer = i2c.readfrom(SCD41_ADDR, 3)

    # Verify CRC
    if crc8(buffer[0:2]) != buffer[2]:
        print("CRC error on data ready status")
        return None
    
    # Check if data is ready (bit 11 of the 16-bit word)
    data_ready = ((buffer[0] << 8) | buffer[1]) & 0x07FF
    if data_ready == 0:
        print("No data ready")
        return None

    # Read measurement
    time.sleep_ms(1)
    i2c.writeto(SCD41_ADDR, bytes([0xEC, 0x05]))
    time.sleep_ms(10)
    buffer = i2c.readfrom(SCD41_ADDR, 9)

    #ormatted_buffer = ' '.join([f'{b:02x}' for b in buffer])
    #print(f"Buffer (hex): {formatted_buffer}")
    return decode_measurement(buffer)




class Scd41:
    def __init__(self, ctx:GlobalContext):
        print("Initializing SCD41")
        self.awaiting_data_since_ticks = 0
        self.last_update_ticks = 0 
        scd41_init(ctx.i2c)
    
    def on_tick(self, ctx:GlobalContext):
        # Measurement update interval is 5s
        if time.ticks_diff(ctx.ticks_ms, self.last_update_ticks) > 6000:
            result = scd41_measure(ctx.i2c)
            if result != None:
                [self.ctx.scd41_temperature, self.ctx.scd41_humidity, self.ctx.scd41_co2 ] = result
            self.last_update_ticks = ctx.ticks_ms

# Make this runnable
if __name__ == "__main__":
    print("Running as standalone script")

    print("Verifying sample data from datasheet (25/37/500)")
    buffer = bytes([0x01, 0xf4, 0x33, 0x66, 0x67, 0xa2, 0x5e, 0xb9, 0x3c])
    [t, h, c] = decode_measurement(buffer)
    print(f"Temp: {t:.2f}C, Hum: {h:.2f}%, CO2:{c}ppm\n")


    from machine import Pin, I2C
    led = Pin("LED", Pin.OUT)
    led.toggle()
    i2c = I2C(0, sda=Pin(0), scl=Pin(1))
    #print("I2C Scan (looking for 98)")
    #i2c.scan()
    print("Initializing measurement")
    scd41_init(i2c)
    print("Measurement loop (expected data every 5s)")
    while(True):
        try:
            time.sleep(1)
            led.toggle()
            result = scd41_measure(i2c)
            if result != None:
                [t, h, c] = result
                print(f"Temp: {t:.2f}C, Hum: {h:.2f}%, CO2:{c}ppm")
        except KeyboardInterrupt:
            break
    print("Done.")
