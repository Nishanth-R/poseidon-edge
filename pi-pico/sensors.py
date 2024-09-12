import machine
import time

# Initialize I2C bus
scl = machine.Pin(1)
sda = machine.Pin(0)
i2c = machine.I2C(0, scl=scl, sda=sda)

class MPRLS:
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x18  # Default I2C address for MPRLS
    
    def read_pressure(self):
        try:
            self.i2c.writeto(self.addr, b'\xF7')  # Send read pressure command
            time.sleep_ms(10)  # Wait for measurement
            data = self.i2c.readfrom(self.addr, 4)  # Read 4 bytes of data
            pressure = (data[0] << 16 | data[1] << 8 | data[2]) / 4096.0
            return pressure
        except Exception as e:
            print(f"Error reading MPRLS: {e}")
            return None

class BNO085:
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x28  # Default I2C address for BNO085
    
    def read_acceleration(self):
        try:
            self.i2c.writeto(self.addr, b'\x08')  # Send read acceleration command
            time.sleep_ms(10)  # Wait for measurement
            data = self.i2c.readfrom(self.addr, 6)  # Read 6 bytes of data
            x = (data[0] << 8 | data[1]) / 100.0
            y = (data[2] << 8 | data[3]) / 100.0
            z = (data[4] << 8 | data[5]) / 100.0
            return x, y, z
        except Exception as e:
            print(f"Error reading BNO085: {e}")
            return None


