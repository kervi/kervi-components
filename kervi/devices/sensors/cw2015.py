from kervi.hal import I2CSensorDeviceDriver
import time


AX17043_ADDR = 0x36
MAX17043_VCELL = 0x02
MAX17043_SOC = 0x04
MAX17043_MODE = 0x06
MAX17043_VERSION = 0x08
MAX17043_CONFIG = 0x0c
MAX17043_COMMAND = 0xfe

class CW2015VoltageDeviceDriver(I2CSensorDeviceDriver):
    def __init__(self, address=0x62, bus=None):
        I2CSensorDeviceDriver.__init__(self, address, bus)
        version = self.i2c.read_U8(0x08)
        self.i2c.write8(0x0a, 0x00)
        print("v", version)
        
    @property
    def device_name(self):
        return "cw2015-voltage"

    @property
    def type(self):
        return "voltage"

    @property
    def unit(self):
        return "v"

    @property
    def max(self):
        return 100

    @property
    def min(self):
        return 0

    def read_value(self):
        v = self.i2c.read_U16(MAX17043_VCELL)
        vr = self.i2c.reverse_byte_order(v)
        
        return  305 * vr / 1000000

class CW2015CapacityDeviceDriver(I2CSensorDeviceDriver):
    def __init__(self, address=0x62, bus=None):
        I2CSensorDeviceDriver.__init__(self, address, bus)
        version = self.i2c.read_U8(0x08)
        self.i2c.write8(0x0a, 0x00)
        print("v", version)
        
    @property
    def device_name(self):
        return "CW2015-capacity"

    @property
    def type(self):
        return "battery"

    @property
    def unit(self):
        return "%"

    @property
    def max(self):
        return 100

    @property
    def min(self):
        return 0

    def read_value(self):
        v1 = self.i2c.read_U8(MAX17043_SOC)
        v2 = self.i2c.read_U8(MAX17043_SOC + 1)
        v = v1 + v2/256
        
        return v

	
	

	    
    
