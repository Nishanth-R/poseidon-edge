from config import wifi_ssid,wifi_password,mqtt_server, mqtt_port
import network
from umqtt.simple import MQTTClient


# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('WiFi connected, IP:', wlan.ifconfig()[0])


# Connect to MQTT broker
def connect_mqtt():
    client = MQTTClient("pico", MQTT_BROKER, MQTT_PORT)
    client.connect()
    print('Connected to MQTT Broker')
    return client


