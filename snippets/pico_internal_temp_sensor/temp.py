import machine
import utime

sensor_pin = 4
sensor_adc = machine.ADC(sensor_pin)
led_pin    = machine.Pin("LED", machine.Pin.OUT)

def sensor_temperature():
    adc_reading = sensor_adc.read_u16() 
    adc_volts   = adc_reading * 3.3 / 65535
    temperature = 27 - (adc_volts - 0.706)/0.001721
    return temperature

def blink_led():
    led_pin.high()
    utime.sleep(.05)
    led_pin.low()

while True:
    try:
        temperature = sensor_temperature()
        print("Temperature:", round(temperature, 2))
        utime.sleep(.45)
        blink_led()
    except KeyboardInterrupt:
        break

led_pin.off()
print("Finished")

