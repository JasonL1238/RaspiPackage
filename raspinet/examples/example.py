# examples/example.py
from raspinet.core import RaspiNet, discover_devices

network = RaspiNet()
# For testing, use localhost instead of discover_devices()
devices = ['127.0.0.1']
print("Available devices:", devices)

if devices:
    network.connect_to_device(devices[0])
    network.send_message("Hello, Raspberry Pi!", devices[0])
    response = network.receive_message(devices[0])
    print("Response:", response)
    network.disconnect_device(devices[0])
