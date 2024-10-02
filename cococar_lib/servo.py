import pigpio
from utils import clamp, remap_range


class Servo:
    def __init__(self, pi, pin, motor_range):
        self._pi = pi
        self._pin = pin
        self._range = motor_range

        # reset position to zero
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.set_servo_pulsewidth(pin, 1500)

    def turn(self, angle: float):
        # check for out of bounds
        angle = clamp(angle, -self._range / 2, self._range / 2)
        pulsewidth = remap_range(angle, -1, 1, 500, 2500)
        self._pi.set_servo_pulsewidth(self._pin, pulsewidth)
