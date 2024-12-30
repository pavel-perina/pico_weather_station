import time, network, urequests

wifi_ssid     = "xxx" 
wifi_password = "xxx"
wifi_max_retries = 5
upload_server = "http://192.168.68.10:5000/upload"

class log_entry:
    def __init__(self):  
        self.temp       = -1234
        self.rh         = 4321
        self.pressure   = 1013250
    def __str__(self):
        str='{{ "station_id": "sta01", "temperature": {:.2f}, "pressure": {:.1f}, "humidity": {:.2f} }}'.format(self.temp*0.01, self.pressure*0.1, self.rh*0.01)
        return str
    
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(wifi_ssid, wifi_password)
        attempts = 0
        while not wlan.isconnected() and attempts < wifi_max_retries:
            time.sleep(2)
            attempts += 1
    return wlan.isconnected()

def send_data():
    try:
        headers = { "Content-Type": "application/json" }
        entry = log_entry() 
        payload = entry.__str__()
        resp = urequests.post(upload_server, data=payload, headers=headers)
        if resp.status_code == 200:
            print("Data posted successfully.")  
        else:
            print("Server error, status:", resp.status_code)
        resp.close()
    except Exception as e:
        print(f"An exception occurred: {e}") 

print("Connecting")
if wifi_connect():
    print("Connected")
    send_data()
else:
    print("Connection failed")
