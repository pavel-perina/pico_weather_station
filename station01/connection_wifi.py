from global_context import GlobalContext
import network
import ntptime
import time
import requests
from collections import deque
from config import wifi_ssid, wifi_password, upload_server

def get_time_str():
    tm = time.localtime()
    return f"{tm[0]}-{tm[1]:02d}-{tm[2]:02d}T{tm[3]:02d}:{tm[4]:02d}:{tm[5]:02d}Z"

STATE_IDLE = 0
STATE_CONNECTING = 1
STATE_UPLOADING = 2

QUEUE_MAX_LEN = 10
QUEUE_FLUSH_LEN = 1#3

# Data sampling interval in seconds
SAMPLING_INTERVAL = 60_000


class Measurement:
    def __init__(self, ctx:GlobalContext):
        self.time = get_time_str()
        self.temperature = ctx.sht40_temperature
        self.humidity = ctx.sht40_humidity
        self.pressure = ctx.bmp280_pressure

class Connection:
    def __init__(self, ctx:GlobalContext):
        self.is_connected = False
        self.last_ntp_sync = 0
        self.wlan = network.WLAN(network.STA_IF)
        self.connection_checked = 0
        self.state = None
        self.enter_state(ctx, STATE_IDLE)
        # Hold 10 measurements, old are overwritten by append
        self.measurements = deque([], QUEUE_MAX_LEN)
        self.last_measurement_ticks = 0

    def enqueue_measurement(self, ctx):
        self.measurements.append(Measurement(ctx))
    
    def connect(self, ctx:GlobalContext):
        print(f"Initializing connection to {wifi_ssid}")
        self.wlan.active(True)
        self.wlan.connect(wifi_ssid, wifi_password)
        self.enter_state(ctx, STATE_CONNECTING)
        self.connection_checked = ctx.ticks_ms
        print(f"State entered: {self.state_entered}")

    def enter_state(self, ctx:GlobalContext, state:int):
        if self.state != state:
            print(f"Connection: Changing state from {self.state} to {state} at {ctx.ticks_ms*.001:.3f} ms uptime")
        self.state = state
        self.state_entered = ctx.ticks_ms
        
    def disconnect(self, ctx:GlobalContext):
        self.wlan.disconnect()
        self.wlan.active(False)
        self.wlan.deinit()
        self.enter_state(ctx, STATE_IDLE)

    def upload_data(self, ctx):
        pass
        
    def sync_time(self, ctx):
        if not self.wlan.isconnected():
            print("sync_time: not connected!")
            return
        tm_old = get_time_str()
        ntptime.host = "tik.cesnet.cz" # optional
        ntptime.settime()
        tm_new = get_time_str()
        print("sync_time: syncing time from " + tm_old + " to " + tm_new)
        self.last_ntp_sync = ctx.ticks_ms

    def on_tick(self, ctx:GlobalContext):
        if (self.state == STATE_IDLE):
            # Enqueue valid measurement on sampling interval
            if time.ticks_diff(ctx.ticks_ms, self.last_measurement_ticks) > SAMPLING_INTERVAL:
                print("========= SAMPLING =============")
                if (ctx.bmp280_pressure > 0):
                    self.enqueue_measurement(ctx)
                self.last_measurement_ticks = ctx.ticks_ms

            # Initiate connection if queue reaches lenght
            if len(self.measurements) >= QUEUE_FLUSH_LEN:
                print("========= SENDING =============")
                self.connect(ctx)
                return
            
        if (self.state == STATE_CONNECTING):
            if time.ticks_diff(ctx.ticks_ms, self.connection_checked) > 250:
                print("Checking connection")
                if self.wlan.isconnected():
                    self.enter_state(ctx, STATE_UPLOADING)
                    try:
                        # Sync time if needed
                        if time.ticks_diff(ctx.ticks_ms, self.last_ntp_sync) > 86_400_000 or self.last_ntp_sync == 0:
                            self.sync_time(ctx)
                        headers = { "Content-Type": "application/json" }
                        while len(self.measurements) > 0: 
                            m:Measurement = self.measurements[0]
                            payload = '{{ "station_id": "sta01", "time": "{}", "temperature": {:.2f}, "pressure": {:.1f}, "humidity": {:.2f} }}' \
                                    .format(m.time, m.temperature , m.pressure, m.humidity)
                            resp = requests.post(upload_server, data=payload, headers=headers)
                            if resp.status_code == 200:
                                print("Data posted successfully.")  
                            else:
                                print("Server error, status:", resp.status_code)
                            # Measurement was received, it it was not accepted, there's no point retrying
                            self.measurements.popleft()
                            resp.close()
                            print(f"Send took {time.ticks_ms() - ctx.ticks_ms}ms")
                    except Exception as e:
                        print(f"An exception occurred: {e}")
                        self.enter_state(ctx, STATE_IDLE)
                    self.disconnect(ctx)
                else:
                    self.connection_checked = ctx.ticks_ms
            if time.ticks_diff(ctx.ticks_ms, self.state_entered) > 15_000 and self.state == STATE_CONNECTING:
                print(f"Ticks: {ctx.ticks_ms}, state entered: {self.state_entered}")
                print("Connection time out")
                self.enter_state(ctx, STATE_IDLE)
                return
