from sensors import MPRLS,BNO085, i2c
import time
from transceive import connect_mqtt,connect_wifi
from config import mqtt_topic

# Initialize sensors
mprls = MPRLS(i2c)
bno085 = BNO085(i2c)

#Connect to Wifi
connect_wifi()
#Connect to MQTT client
client = connect_mqtt()


def send_message(client, payload):
    client.publish(mqtt_topic, payload)
    print('Published message : '+payload)
    

while True:
    try:
        pressure = mprls.read_pressure()
        accel_x, accel_y, accel_z = bno085.read_acceleration()
        
        if pressure is not None and accel_x is not None:
            # Send data via MQTT
            payload = 'pressure:'+str(pressure)+'||acceleration:'+str([accel_x,accel_y,accel_z])

            print(f"Pressure: {pressure:.2f} kPa")
            print(f"Acceleration: X={accel_x:.2f}, Y={accel_y:.2f}, Z={accel_z:.2f} m/s^2")
            print(payload) 
            send_message(client, payload)
        else:
            print('Did not receive data from Sensor') 
        time.sleep(1) #Keep the delay as 1s, lower values is causing some comms issue on the I2C side
    
    except KeyboardInterrupt:
        print("Program interrupted by user.")
        break
    
    except Exception as e:
        print(f"An error occurred: {e}")

