
# Poseidon pico sensor publisher 

This master directory contains the code to read data from 2 sensors 
1. Adafruit MPRLS Pressure sensor -> https://cdn-learn.adafruit.com/downloads/pdf/adafruit-mprls-ported-pressure-sensor-breakout.pdf
2. Adafruit BNO085 IMU -> https://cdn-learn.adafruit.com/downloads/pdf/adafruit-9-dof-orientation-imu-fusion-breakout-bno085.pdf

### Message format 

`pressure:1024.0||acceleration:[426.24, 0.55, 285.24]`

## Description
The code initialises the I2C connections to the two sensors on the below addresses - 
    1. MPRLS - 0x18
    2. BNO085 - 0x4a
Once the sensors are initialised, the code reads the two sensors once a second and sends data to a topic `poseidon`. Subscribing to this topic will give data in the message format above. 

## Initilisation 
Copy files as is to the pico W using thonny. If you are using pico W for the first time hit the BOOTSEL button while plugging the micro usb cable for the first time. Follow instructions here -> https://randomnerdtutorials.com/getting-started-raspberry-pi-pico-w/

## Sensor Circuit Diagram 
![circuit](https://github.com/user-attachments/assets/285bdc15-825a-4d0b-95c5-15ca7bfefae5)
