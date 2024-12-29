import time
import bluetooth
import struct
from micropython import const

# BLE event constants
_IRQ_CENTRAL_CONNECT    = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

# Standard BLE UUIDs for Environmental Sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_TEMP_CHAR_UUID = bluetooth.UUID(0x2A6E)  # Temperature Characteristic
_HUM_CHAR_UUID  = bluetooth.UUID(0x2A6F)  # Humidity Characteristic
_PRESS_CHAR_UUID= bluetooth.UUID(0x2A6D)  # Pressure Characteristic

# Flags for read and notify
_FLAG_READ  = const(0x0001)
_FLAG_NOTIFY= const(0x0010)

# Prepare the GATT server structure
environment_sense_service = (
    _ENV_SENSE_UUID,
    (
        (_TEMP_CHAR_UUID,  _FLAG_READ | _FLAG_NOTIFY),
        (_HUM_CHAR_UUID,   _FLAG_READ | _FLAG_NOTIFY),
        (_PRESS_CHAR_UUID, _FLAG_READ | _FLAG_NOTIFY),
    ),
)

# Advertisement helper for BLE
def advertise(ble, name="PicoW-Env"):
    # A simple advertisement for discoverability
    # Including flags and name
    adv_data = bytearray(
        b"\x02\x01\x06"              # Flags indicating BLE general discoverable
        + bytes([len(name) + 1, 0x09])  # Complete local name
        + name.encode()
    )
    ble.gap_advertise(100_000, adv_data)

class BLEEnvSense:
    def __init__(self, ble):
        self._counter = 0
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)

        # Holds the connection handle when a central device is connected
        self._conn_handle = None
        
        # Create a GATT server and register the Environmental Sensing service
        ((self._temp_handle, self._hum_handle, self._press_handle),) = self._ble.gatts_register_services((environment_sense_service,))
        
        # Start advertising
        advertise(self._ble)
    
    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            # A central connected
            conn_handle, addr_type, addr = data
            self._conn_handle = conn_handle

        elif event == _IRQ_CENTRAL_DISCONNECT:
            # A central disconnected
            conn_handle, addr_type, addr = data
            if conn_handle == self._conn_handle:
                self._conn_handle = None

    def update_values(self):
        # Trial-error fixed point values found values for -12.34C, 43.21% RH, 101325.0Pa
        temp_bytes = struct.pack('<i', -1234 + self._counter)
        hum_bytes  = struct.pack('<i', 4321 + self._counter)
        press_bytes= struct.pack('<i', 1013250 + self._counter)
        self._counter += 1

        self._ble.gatts_write(self._temp_handle, temp_bytes)
        self._ble.gatts_write(self._hum_handle, hum_bytes)
        self._ble.gatts_write(self._press_handle, press_bytes)

        # Notify only if there is a valid connection
        if self._conn_handle is not None:
            self._ble.gatts_notify(self._conn_handle, self._temp_handle)
            self._ble.gatts_notify(self._conn_handle, self._hum_handle)
            self._ble.gatts_notify(self._conn_handle, self._press_handle)

def main():
    counter=0
    ble = bluetooth.BLE()
    print("BLE created")
    env_sense = BLEEnvSense(ble)
    print("BLEEnvSense created")
    while True:
        # Update BLE characteristics with constants for demonstration
        env_sense.update_values()
        
        # Delay before updating again
        time.sleep(5)

if __name__ == "__main__":
    main()
