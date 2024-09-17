import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")  # Subscribe to all topics

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

# Create an MQTT client and attach our callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect("localhost", 1883, 60)

# Start the loop
client.loop_forever()
