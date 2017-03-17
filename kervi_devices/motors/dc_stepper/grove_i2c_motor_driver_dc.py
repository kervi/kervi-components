

from kervi.hal import i2c
from kervi.hal.dc_motor_controller import DCMotorControllerBase

MOTOR_SPEED_SET = 0x82
PWM_FREQUENCE_SET = 0x84
DIRECTION_SET = 0xaa
MOTOR_SET_A = 0xa1
MOTOR_SET_B = 0xa5
NOTHING = 0x01
ENABLE_STEPPER = 0x1a
UNENABLE_STEPPER = 0x1b
STEPERNU = 0x1c
I2C_MOTOR_DRIVER_ADD = 0x0f #Set the address of the I2CMotorDriver

BOTH_CLOCK_WISE = 0x0a
BOTH_ANTI_CLOCK_WISE = 0x05
M1_CW_M2_ACW = 0x06
M1_ACW_M2CW = 0x09

class MotorDeviceDriver(DCMotorControllerBase):
    def __init__(self, address=I2C_MOTOR_DRIVER_ADD, bus=None):
        DCMotorControllerBase.__init__(self, "Grove i2c motor driver", 2)
        self.i2c = i2c(address, bus)
        self.m1_speed = 0
        self.m2_speed = 0

        self.m1_direction = 1
        self.m2_direction = 1

    def _map(self, x, in_min, in_max, out_min, out_max):
        return abs(int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min))

    def _set_speed(self, motor, speed):
        if motor == 1:
            self.m1_speed = self._map(speed, 0, 100, 0, 255)
            if speed >= 0:
                self.m1_direction = 1
            else:
                self.m1_direction = -1

        else:
            self.m2_speed = self._map(speed, 0, 100, 0, 255)
            if speed >= 0:
                self.m2_direction = 1
            else:
                self.m2_direction = -1

        if self.m1_direction == 1 and self.m2_direction == 1:
            direction = BOTH_CLOCK_WISE
        if self.m1_direction == 1 and self.m2_direction == -1:
            direction = M1_CW_M2_ACW
        if self.m1_direction == -1 and self.m2_direction == 1:
            direction = M1_ACW_M2CW
        if self.m1_direction == -1 and self.m2_direction == -1:
            direction = BOTH_ANTI_CLOCK_WISE

        self.i2c.write_list(MOTOR_SPEED_SET, [self.m1_speed, self.m2_speed])
        self.i2c.write_list(DIRECTION_SET, [direction, NOTHING])
