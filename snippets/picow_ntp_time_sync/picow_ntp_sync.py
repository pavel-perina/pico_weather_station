import network
import ntptime
import time

# Known networks with corresponding passwords
known_networks = {
    'YourSSID': 'YourPassword',
    'public': "",
}

def sync_time():
    print("Synchronizing time via NTP ...")
    ntptime.host = "tik.cesnet.cz" # optional
    ntptime.settime()

def wifi_try_connect():
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    scanned = wlan.scan()
    found = False
    for entry in scanned:
        ssid_str = entry[0].decode()
        if ssid_str in known_networks:
            print(f"Found known SSID: {ssid_str}")
            found = True
            wlan.connect(ssid_str, known_networks[ssid_str])
            # Wait a few seconds to see if it connects
            print ("Connecting: ", end='')
            for _ in range(20):
                if wlan.isconnected():
                    break
                time.sleep_ms(500)
                print(".", end='')
            print()

    if wlan.isconnected():
        print("Connected successfully.")
        return True
    else:
        if not found:
            print("Known wifi connection was not found.")
        print("Connection attempt failed.")
        return False

if wifi_try_connect():
    sync_time()
    print(time.localtime())
