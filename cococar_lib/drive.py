import pigpio
# import random
from .utils import clamp


def _speed_to_pulsewidth(speed, min_us, max_us):
    ratio = (speed + 1) / 2
    return round(min_us + (max_us - min_us) * ratio)


class Drive:
    def __init__(self, pi, left_pin, right_pin, min_us, max_us, left_offset=0, right_offset=0, wheel_diameter=3.75):
        self._pi = pi
        self._left_pin = left_pin
        self._right_pin = right_pin
        self._min_us = min_us
        self._max_us = max_us
        self._left_offset = left_offset
        self._right_offset = right_offset
        self._wheel_diameter = wheel_diameter

        for output_pin in [left_pin, right_pin]:
            pi.set_mode(output_pin, pigpio.OUTPUT)
            pi.set_servo_pulsewidth(output_pin, _speed_to_pulsewidth(0, min_us, max_us))
            pi.set_servo_pulsewidth(output_pin, _speed_to_pulsewidth(0, min_us, max_us))

    def set_speed(self, left_speed, right_speed):
        left_clamped = clamp(left_speed, -1, 1)
        right_clamped = clamp(right_speed, -1, 1)

        # left_offset = self._left_offset + (1 if random.randint(0, 10) > 4 else 0)
        left_offset = self._left_offset
        right_offset = self._right_offset

        self._pi.set_servo_pulsewidth(self._left_pin, _speed_to_pulsewidth(left_clamped, self._min_us, self._max_us) + left_offset)
        self._pi.set_servo_pulsewidth(self._right_pin, _speed_to_pulsewidth(right_clamped, self._min_us, self._max_us) + right_offset)
