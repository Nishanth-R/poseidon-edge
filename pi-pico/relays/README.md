# Poseidon pico listner

This directory contains all the code required to run a mqtt listner to subscribe to topic `poseidon-act` where it will listen to string messages. 

### Sample message

`bilge:true||drain:false||wake:false`


### Sample mosquitto publish command 
```mosquitto_pub -h 192.168.0.55 -t "poseidon-act" -m "bilge:true||drain:true||wake:false "```

## Description
When `bilge` is true, it sends a command to pull relay to ON position. When it is false bilge relay is OFF 

When `drain` is true, it sends a command to pull relay to ON position. When it is false bilge relay is OFF 

When `wake` is true, it sends a pulse to the raspberry pi 5. 
When coordinated with the boot-config file in 
https://github.com/Nishanth-R/poseidon-edge/blob/main/raspberry-pi/boot/config.txt It will send a pulse to PIN GPIO26 of the Pi5 to wake it up. 

## Initilisation 
Copy files as is to the pico W using thonny. 
If you are using pico W for the first time hit the BOOTSEL button while plugging the micro usb cable for the first time. 
Follow instructions here -> https://randomnerdtutorials.com/getting-started-raspberry-pi-pico-w/

## Circuit Diagram 
![circuit (1)](https://github.com/user-attachments/assets/a8bea16c-52ba-4e1e-9a2b-8fa2d356e3b0)
