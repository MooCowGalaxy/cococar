import pigpio


def _us_to_ratio(us, min_us, max_us):
    return max(min((us - min_us) / (max_us - min_us), 1), 0)


def _ratio_to_speed(ratio):
    return -1 + ratio * 2


class Controller:
    LEFT_X = 4
    LEFT_Y = 3
    RIGHT_X = 1
    RIGHT_Y = 2

    def __init__(self, pi, input_pins, min_us, max_us):
        self._pi = pi
        self._input_pins = input_pins
        self._channel_values = {}
        self._start_time = {}
        self._min_us = min_us
        self._max_us = max_us

        for input_pin in input_pins:
            self._start_time[input_pin] = None
            pi.callback(input_pin, pigpio.EITHER_EDGE, self._callback)

    def _callback(self, gpio, level, tick):
        if level == 0 and self._start_time[gpio] is not None:
            # gpio went from 1 to 0
            us = tick - self._start_time[gpio]
            self._channel_values[gpio] = _us_to_ratio(us, self._min_us, self._max_us)
            self._start_time[gpio] = None

        elif level == 1 and self._start_time[gpio] is None:
            self._start_time[gpio] = tick

    def get_channel(self, channel):
        if self._input_pins[channel - 1] not in self._channel_values:
            return 0

        value = self._channel_values[self._input_pins[channel - 1]]

        if channel in [self.LEFT_X, self.RIGHT_X, self.RIGHT_Y]:
            value = _ratio_to_speed(value)

        if abs(value) < 0.02:  # remove noise
            value = 0

        return value
