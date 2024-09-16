import network
import ujson
from umqtt.robust import MQTTClient
from machine import Pin, reset
import time
import random

# Wi-Fi credentials
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

# MQTT settings
MQTT_BROKER = "YOUR_MQTT_BROKER_ADDRESS"
MQTT_TOPIC = b"poseidon-act"
MQTT_CLIENT_ID = f"pico_client_{random.randint(0, 1000000)}"

# GPIO pin assignments
BILGE_RELAY_PIN = 16
DRAIN_RELAY_PIN = 17
WAKE_PI_PIN = 18

# Initialize pins
bilge_relay = Pin(BILGE_RELAY_PIN, Pin.OUT)
drain_relay = Pin(DRAIN_RELAY_PIN, Pin.OUT)
wake_pi = Pin(WAKE_PI_PIN, Pin.OUT)

# Global variables
mqtt_client = None
wlan = None

def connect_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        for _ in range(100):  # Wait up to 10 seconds for connection
            if wlan.isconnected():
                break
            time.sleep(0.1)
    if wlan.isconnected():
        print("Connected to Wi-Fi")
        print("IP address:", wlan.ifconfig()[0])
    else:
        print("Failed to connect to Wi-Fi")
        return False
    return True

def mqtt_callback(topic, msg):
    print("Received message on topic:", topic)
    print("Message:", msg)
    
    try:
        data = ujson.loads(msg)
        
        # Control relays
        if data.get('bilge') and not data.get('drain'):
            bilge_relay.on()
            drain_relay.off()
        elif data.get('drain') and not data.get('bilge'):
            drain_relay.on()
            bilge_relay.off()
        else:
            bilge_relay.off()
            drain_relay.off()
        
        # Wake up Raspberry Pi 5
        if data.get('wake'):
            wake_raspberry_pi()
    
    except ValueError as e:
        print("Error parsing JSON:", e)

def wake_raspberry_pi():
    print("Waking up Raspberry Pi 5...")
    wake_pi.on()
    time.sleep(0.1)  # Send a 100ms pulse
    wake_pi.off()

def connect_mqtt():
    global mqtt_client
    mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, keepalive=30)
    mqtt_client.set_callback(mqtt_callback)
    try:
        mqtt_client.connect()
        mqtt_client.subscribe(MQTT_TOPIC)
        print(f"Connected to MQTT broker, subscribed to {MQTT_TOPIC}")
        return True
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return False

def main():
    while True:
        if not wlan or not wlan.isconnected():
            if not connect_wifi():
                time.sleep(10)
                continue

        if not mqtt_client or not mqtt_client.is_connected():
            if not connect_mqtt():
                time.sleep(10)
                continue

        try:
            mqtt_client.check_msg()
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in main loop: {e}")
            mqtt_client.disconnect()
            time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Critical error: {e}")
        time.sleep(10)
        reset()  # Reset the Pico if there's a critical error
