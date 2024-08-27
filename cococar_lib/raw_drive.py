import pigpio
from .utils import clamp


def _speed_to_pulsewidth(speed, min_us, max_us):
    ratio = (speed + 1) / 2
    return round(min_us + (max_us - min_us) * ratio)


class RawDrive:
    def __init__(self, pi, left_pin, right_pin, min_us, max_us, max_speed=0.8):
        self._pi = pi
        self._left_pin = left_pin
        self._right_pin = right_pin
        self._min_us = min_us
        self._max_us = max_us
        self._max_speed = max_speed

        for output_pin in [left_pin, right_pin]:
            pi.set_mode(output_pin, pigpio.OUTPUT)
            pi.set_servo_pulsewidth(output_pin, _speed_to_pulsewidth(0, min_us, max_us))
            pi.set_servo_pulsewidth(output_pin, _speed_to_pulsewidth(0, min_us, max_us))

    def set_speed(self, left_speed, right_speed):
        left_clamped = clamp(left_speed, -self._max_speed, self._max_speed)
        right_clamped = clamp(right_speed, -self._max_speed, self._max_speed)

        self._pi.set_servo_pulsewidth(self._left_pin, _speed_to_pulsewidth(left_clamped, self._min_us, self._max_us))
        self._pi.set_servo_pulsewidth(self._right_pin, _speed_to_pulsewidth(right_clamped, self._min_us, self._max_us))
